# DOCUMENT VERIFIER — Powered by Deep Learning

> **QUANTIX 2K26 — 24-Hour Hackathon Project**  
> **Developed by Deepak & Team**  
> **Mission:** Provide AI-assisted document screening, multi-stage OCR entity extraction, explainable image-forensics tampering detection, and reference-record cross-examination with deterministic, defensible outcomes.

---

## 📑 Table of Contents
1. [Executive Summary](#executive-summary)
2. [Key Features](#key-features)
3. [Visual Design & Theme](#visual-design--theme)
4. [Verification Decision Engine](#verification-decision-engine)
5. [System Architecture](#system-architecture)
6. [Hackathon Demo Center](#hackathon-demo-center)
7. [Installation & Setup](#installation--setup)
8. [Live Camera Scanner Guide](#live-camera-scanner-guide)
9. [Automated Test Suite](#automated-test-suite)
10. [Privacy & Security Policy](#privacy--security-policy)
11. [Limitations & Ethical Considerations](#limitations--ethical-considerations)
12. [Project File Structure](#project-file-structure)

---

## 🔍 Executive Summary

Credential and certificate fraud is an escalating challenge for universities, employers, and government institutions. While physical credentials may contain seals, digital uploads (PDFs, scans, camera captures) are frequently subject to image manipulation, spliced designations, altered marks, or forged names.

**DOCUMENT VERIFIER** is an offline, laptop-first cybersecurity and computer vision application built specifically for a live college hackathon demonstration at **QUANTIX 2K26**. It unifies:
- **Optical Character Recognition (OCR):** Multi-engine cascade (Windows native neural OCR, PyPDF vector extraction, and Tesseract support) extracting structured document fields (Title, Holder Name, Document ID, Issue Date, Issuer).
- **Explainable Image Forensics:** Error Level Analysis (ELA), high-frequency noise variance, and gradient edge discontinuity detection to identify pasted patches without black-box guesswork.
- **Reference Database Matching:** SQLite database containing synthetic demo records and simulated authoritative issuer ledgers.
- **Explainable Decision Engine:** Strict evidence rules yielding three distinct outcomes with full auditability and PDF report downloads.

---

## 🚀 Key Features

- **Multi-Format Ingestion:** Drag-and-drop support for PDF, PNG, JPG, and JPEG documents up to 15 MB.
- **Live Laptop Webcam Scanner:** Uses the browser `MediaDevices` API (`getUserMedia`) with an interactive document-shaped guide frame, real-time lighting/blur diagnostics, perspective transform, and auto-cropping.
- **Editable OCR Fields:** Users can review and adjust extracted fields in real-time before triggering case re-evaluation.
- **Forensic Anomaly Heatmap:** Visual side-by-side / overlay toggle highlighting localized JPEG compression discrepancies (ELA).
- **Demo Reference Database:** Built-in CRUD interface to add, view, and test against synthetic reference records.
- **Downloadable PDF Audit Certificates:** Clean, branded PDF reports containing case metadata, SHA-256 hashes, field comparisons, and forensic checklists.
- **100% Offline Laptop Execution:** Requires zero external cloud APIs or GPUs. Runs cleanly on modern Windows laptops.

---

## 🎨 Visual Design & Theme

- **Palette:** Deep Navy background (`#07111F`), dark blue cards (`#0B192C`, `#0F233D`), vibrant cyan highlights (`#00E5FF`), and crisp white typography (`#F8FAFC`).
- **Styling:** Glassmorphism panels, subtle borders (`rgba(0, 229, 255, 0.25)`), smooth transitions, high-contrast accessible typography, and keyboard navigation.
- **Display:** Optimized for live laptop presentations before hackathon judges, fully responsive on mobile devices.

---

## ⚖️ Verification Decision Engine

The system strictly enforces evidence-based outcome rules and avoids speculative confidence scores:

| Verification Outcome | Meaning & Strict Rule Trigger |
| :--- | :--- |
| <span style="color:#10B981; font-weight:bold;">REAL — VERIFIED</span> | Document identifier and holder credentials **match an authoritative issuing registry ledger** and **zero forensic tampering anomalies** are detected. Local demo cache matches do NOT qualify. |
| <span style="color:#EF4444; font-weight:bold;">FAKE — EVIDENCE FOUND</span> | Reliable evidence of fraud is uncovered: **Registry identity conflict** (e.g., ID is registered to another individual or status is REVOKED) OR **corroborating forensic tampering** (ELA compression mismatch + spliced edge boundaries + editing software footprint). |
| <span style="color:#F59E0B; font-weight:bold;">SUSPICIOUS — MANUAL REVIEW REQUIRED</span> | Default safe outcome for inconclusive cases: Document matches local synthetic demo cache but lacks authoritative source; unregistered documents; severe image blur / motion defocus; or low OCR extraction confidence. |

---

## 🏗️ System Architecture

```
                                 DOCUMENT VERIFIER PIPELINE
                                
  [ Laptop Webcam / Upload ] ───► [ Format & MIME Validator ]
                                            │
                                            ▼
                           [ OpenCV Image Preprocessing ]
                           (Bilateral Filter, CLAHE, Deskew)
                                            │
               ┌────────────────────────────┴───────────────────────────┐
               ▼                                                        ▼
   [ Multi-Engine OCR ]                                     [ Forensics Engine ]
   • Windows.Media.Ocr                                      • Error Level Analysis (ELA)
   • PyPDF Vector Extraction                                • Noise Variance Dispersion
   • PyTesseract Fallback                                   • Splicing Edge Discontinuities
               │                                            • EXIF & Software Footprints
               ▼                                                        │
   [ Structured Field Parser ]                                          │
   (Doc Type, ID, Name, Date, Issuer)                                   │
               │                                                        │
               ▼                                                        │
   [ SQLite Reference DB Lookup ]                                       │
   (Exact & Fuzzy Normalized Match)                                     │
               │                                                        │
               └────────────────────────────┬───────────────────────────┘
                                            ▼
                           [ Deterministic Decision Engine ]
                           ├── REAL — VERIFIED
                           ├── FAKE — EVIDENCE FOUND
                           └── SUSPICIOUS — MANUAL REVIEW REQUIRED
                                            │
                                            ▼
                   [ Interactive Dashboard & PDF / JSON Reports ]
```

---

## ⚡ Hackathon Demo Center

Under the **Demo Documents** tab, judges can test all three outcomes with a single click:

1. **Sample 1: Authoritative Verified Certificate (`REAL — VERIFIED`)**
   - *Document:* KSR Institute of Technology B.E. Degree for Deepak Kumar (`KSR-2026-ENG-8492`).
   - *Outcome:* Authenticity confirmed against authoritative simulated registrar ledger with zero tampering.
2. **Sample 2: Altered Identity / Field Mismatch (`FAKE — EVIDENCE FOUND`)**
   - *Document:* National ID Card with altered name "Robert Vance".
   - *Outcome:* Document ID `NAT-2026-ID-4410` is registered to "Priya Sharma". Critical identity conflict detected.
3. **Sample 3: Digitally Tampered / Spliced Patch (`FAKE — EVIDENCE FOUND`)**
   - *Document:* Experience Certificate with pasted high-rank designation and Adobe Photoshop metadata.
   - *Outcome:* Severe ELA compression anomalies and spliced rectangular edge boundaries detected.
4. **Sample 4: Blurry / Degraded Scan (`SUSPICIOUS — MANUAL REVIEW REQUIRED`)**
   - *Document:* Academic transcript with heavy motion blur.
   - *Outcome:* Image quality too degraded for automated verification. Prompts re-scan.
5. **Sample 5: Unregistered Unknown Document (`SUSPICIOUS — MANUAL REVIEW REQUIRED`)**
   - *Document:* Visually clean certificate from an unregistered private academy.
   - *Outcome:* No matching record found in trusted repositories. Absence of tampering does not certify authenticity.

---

## 🛠️ Installation & Setup

### Prerequisites
- Windows 10 or 11 (Supports native `Windows.Media.Ocr` engine out of the box)
- Python 3.10+ (Tested and verified on Python 3.14.6)
- Modern web browser (Edge, Chrome, Firefox)

### Setup Steps
```powershell
# 1. Navigate to project folder
cd "d:\ksr college project deepak and their team"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch application
python run.py
```

Open your browser and navigate to:
```
http://127.0.0.1:8000
```

---

## 📷 Live Camera Scanner Guide

1. Click on **Live Camera Scan** in the top navigation.
2. Click **▶ Start Camera** and grant browser permission when prompted.
3. Position the credential inside the cyan guide frame.
4. The real-time guidance badge will notify you if lighting is too dim or if glare is detected.
5. Click **📸 Capture Document**.
6. Review the captured frame or click **🔄 Retake** if needed.
7. Click **⚡ Verify Captured Document** to execute the pipeline.

> *Note on Camera Permissions:* Modern web browsers require either `localhost` (`http://127.0.0.1:8000`) or `HTTPS` to access webcam streams. If camera access is denied, use the file upload feature.

---

## 🧪 Automated Test Suite

The project includes an end-to-end automated test suite covering decision logic, OCR parsing, forensics, database matching, and API endpoints:

```powershell
# Run full pytest suite
python -m pytest -v
```

### Verified Test Summary
- `tests/test_decision_engine.py`: Tests `REAL`, `FAKE`, and `SUSPICIOUS` outcome triggers.
- `tests/test_ocr.py`: Tests entity extraction, name sanitization, and missing field alerts.
- `tests/test_reference_db.py`: Tests normalized fuzzy matching and registry conflict detection.
- `tests/test_forensics.py`: Tests sharpness metrics, ELA computation, and noise dispersion.
- `tests/test_api.py`: Tests FastAPI endpoints, health check, and one-click demo loaders.
- **Results:** 24 passed in 3.4 seconds.

---

## 🔒 Privacy & Security Policy

1. **Local Isolation:** All documents, camera frames, and database records remain exclusively on the local machine. No data is transmitted to third-party cloud services.
2. **Safe File Handling:** Filenames are sanitized with regex to prevent directory traversal attacks. File uploads are validated against strict MIME types and a 15 MB size threshold.
3. **Prompt Injection Defense:** OCR extracted text is strictly treated as data payloads and is never passed to generative LLM system prompts as executable commands.
4. **Parameterized SQL:** All database interactions use parameterized SQLite queries (`?` bindings) to prevent SQL injection.

---

## ⚠️ Limitations & Ethical Considerations

- **Decision Support Tool:** This system provides automated screening support. It does not replace official, legally binding verification from authorized credential issuers.
- **Synthetic Test Data:** All pre-packaged demo records and certificates are synthetic examples created for hackathon demonstration. No real personal information is used.
- **Heuristic Indicators vs. Proof:** Forensic anomalies (such as compression artifacts or localized noise variations) indicate candidate tampering areas but do not constitute legal proof of fraud on their own.

---

## 📂 Project File Structure

```
d:\ksr college project deepak and their team\
├── app/
│   ├── __init__.py
│   ├── config.py                 # Application constants, paths & thresholds
│   ├── database.py               # SQLite schema, case audit logs & queries
│   ├── demo_data.py              # Synthetic demo samples & DB seeders
│   ├── ocr_engine.py             # Windows.Media.Ocr, PyPDF & regex parser
│   ├── forensics.py              # ELA, noise analysis, blur & heatmap generator
│   ├── reference_db.py           # Registry matching & fuzzy similarity
│   ├── decision_engine.py        # Strict 3-outcome verification engine
│   ├── report_generator.py       # FPDF PDF report & JSON export
│   ├── camera_helper.py          # Webcam frame processing & perspective warp
│   ├── main.py                   # FastAPI application & REST endpoints
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css         # Deep Navy cyber-AI dashboard styling
│   │   ├── js/
│   │   │   ├── app.js            # Single-page application controller
│   │   │   └── camera.js         # Camera stream & guide frame manager
│   │   └── samples/              # Generated high-res synthetic certificates
│   └── templates/
│       └── index.html            # Complete HTML5 semantic layout
├── tests/
│   ├── test_decision_engine.py   # Decision logic unit tests
│   ├── test_ocr.py               # OCR parser unit tests
│   ├── test_reference_db.py      # Reference matching unit tests
│   ├── test_forensics.py         # Image forensics unit tests
│   └── test_api.py               # FastAPI integration tests
├── storage/
│   ├── uploads/                  # Temporary file upload repository
│   └── reports/                  # Generated PDF & JSON case certificates
├── .env.example                  # Environment configuration template
├── requirements.txt              # Documented Python dependencies
├── run.py                        # Single-command application launcher
└── README.md                     # Comprehensive project documentation
```

---

*Developed by Deepak & Team for QUANTIX 2K26 — 24-Hour Hackathon.*
