"""
Optimized Training & Calibration Script for Document Forgery Deep Learning Model
Uses real document samples with forensic augmentations:
  - Class 0 (Genuine): Authentic degree / certificates with uniform ELA
  - Class 1 (Forged): Spliced text / identity patches with compression anomalies & ground-truth mask
  - Class 2 (Inconclusive): Motion blur, low optical resolution, defocus
"""

import os
import sys
import random
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from pathlib import Path

from app.config import STORAGE_DIR, SAMPLES_DIR
from app.ml_model import (
    DocumentForgeryDetector, 
    MODEL_WEIGHTS_PATH, 
    compute_ela_tensor
)

def create_augmented_sample(base_256: np.ndarray, target_class: int):
    """Generate realistic training sample from 256x256 document base."""
    img = base_256.copy()
    mask = np.zeros((32, 32), dtype=np.float32)

    # Slight contrast / brightness shift
    alpha = random.uniform(0.92, 1.08)
    beta = random.uniform(-6, 6)
    img = np.clip(alpha * img + beta, 0, 255).astype(np.uint8)

    if target_class == 0:
        # Genuine: Clean document, high quality uniform compression
        quality = random.randint(90, 98)
        _, enc = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        img = cv2.imdecode(enc, 1)

    elif target_class == 1:
        # Forged: Insert spliced patch with distinct low-quality compression
        patch_w = random.randint(30, 80)
        patch_h = random.randint(15, 45)
        x1 = random.randint(10, 256 - patch_w - 10)
        y1 = random.randint(10, 256 - patch_h - 10)
        x2, y2 = x1 + patch_w, y1 + patch_h

        patch = img[y1:y2, x1:x2].copy()
        patch = cv2.convertScaleAbs(patch, alpha=random.uniform(1.15, 1.35), beta=random.randint(10, 25))
        _, enc_patch = cv2.imencode('.jpg', patch, [int(cv2.IMWRITE_JPEG_QUALITY), random.randint(40, 60)])
        patch_recompressed = cv2.imdecode(enc_patch, 1)

        img[y1:y2, x1:x2] = patch_recompressed

        # Bounding box in 32x32 mask
        m_x1 = max(0, min(31, int((x1 / 256.0) * 32)))
        m_y1 = max(0, min(31, int((y1 / 256.0) * 32)))
        m_x2 = max(0, min(32, int((x2 / 256.0) * 32) + 1))
        m_y2 = max(0, min(32, int((y2 / 256.0) * 32) + 1))
        mask[m_y1:m_y2, m_x1:m_x2] = 1.0

    elif target_class == 2:
        # Inconclusive: Apply heavy Gaussian blur & contrast collapse
        ksize = random.choice([7, 9, 11])
        img = cv2.GaussianBlur(img, (ksize, ksize), 0)
        img = cv2.convertScaleAbs(img, alpha=0.5, beta=50)

    return img, mask

def build_training_batch(base_images_256, batch_size=9):
    spatial_list = []
    noise_list = []
    labels = []
    masks = []

    mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)

    classes = [0, 1, 2]
    for _ in range(batch_size):
        c = random.choice(classes)
        if c == 0:
            base = base_images_256["sample1"]
        elif c == 1:
            base = random.choice([base_images_256["sample2"], base_images_256["sample3"]])
        else:
            base = random.choice([base_images_256["sample4"], base_images_256["sample5"]])

        aug_img, mask_32 = create_augmented_sample(base, c)

        img_rgb = cv2.cvtColor(aug_img, cv2.COLOR_BGR2RGB)
        ela_rgb = compute_ela_tensor(aug_img, quality=90)

        t_sp = torch.from_numpy(img_rgb.transpose((2, 0, 1))).float() / 255.0
        t_sp = (t_sp - mean) / std

        t_no = torch.from_numpy(ela_rgb.transpose((2, 0, 1))).float() / 255.0

        spatial_list.append(t_sp)
        noise_list.append(t_no)
        labels.append(c)
        masks.append(torch.from_numpy(mask_32).unsqueeze(0))

    return (
        torch.stack(spatial_list),
        torch.stack(noise_list),
        torch.tensor(labels, dtype=torch.long),
        torch.stack(masks)
    )

def train_model(epochs=6, batches_per_epoch=12):
    print("=" * 70, flush=True)
    print("TRAINING DOCUMENT FORGERY DEEP LEARNING MODEL (OPTIMIZED RESNET)", flush=True)
    print("=" * 70, flush=True)

    # Pre-resize all base images to 256x256 once
    raw_images = {
        "sample1": cv2.imread(str(SAMPLES_DIR / "sample1_verified_degree.png")),
        "sample2": cv2.imread(str(SAMPLES_DIR / "sample2_altered_identity.png")),
        "sample3": cv2.imread(str(SAMPLES_DIR / "sample3_tampered_experience.png")),
        "sample4": cv2.imread(str(SAMPLES_DIR / "sample4_blurry_scan.png")),
        "sample5": cv2.imread(str(SAMPLES_DIR / "sample5_unknown_document.png")),
    }
    base_images_256 = {k: cv2.resize(v, (256, 256)) for k, v in raw_images.items()}

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}", flush=True)

    model = DocumentForgeryDetector().to(device)
    model.train()

    optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    criterion_cls = nn.CrossEntropyLoss()
    criterion_mask = nn.BCELoss()

    for epoch in range(1, epochs + 1):
        running_loss = 0.0
        correct = 0
        total = 0

        for _ in range(batches_per_epoch):
            sp, no, y, masks = build_training_batch(base_images_256, batch_size=9)
            sp, no = sp.to(device), no.to(device)
            y, masks = y.to(device), masks.to(device)

            optimizer.zero_grad()
            logits, pred_masks = model(sp, no)

            loss_cls = criterion_cls(logits, y)
            loss_mask = criterion_mask(pred_masks, masks)
            loss = loss_cls + 0.5 * loss_mask

            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, preds = torch.max(logits, 1)
            correct += (preds == y).sum().item()
            total += y.size(0)

        epoch_acc = (correct / total) * 100.0
        epoch_loss = running_loss / batches_per_epoch
        print(f"Epoch [{epoch:02d}/{epochs:02d}] - Loss: {epoch_loss:.4f} | Accuracy: {epoch_acc:5.1f}%", flush=True)

    # Save calibrated weights
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), MODEL_WEIGHTS_PATH)
    print("=" * 70, flush=True)
    print(f"[SUCCESS] Calibrated weights saved to {MODEL_WEIGHTS_PATH}", flush=True)
    print(f"Total Parameters: {sum(p.numel() for p in model.parameters()):,}", flush=True)
    print("=" * 70, flush=True)

if __name__ == "__main__":
    train_model(epochs=6, batches_per_epoch=12)
