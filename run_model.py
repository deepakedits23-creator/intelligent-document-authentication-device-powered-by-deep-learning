"""
Interactive Runner for the PyTorch Document Forgery Deep Learning Model
Run:
    python run_model.py
or
    python run_model.py <path_to_image>
"""

import sys
import time
from pathlib import Path
from app.ml_model import (
    run_deep_learning_inference,
    get_model_summary,
    MODEL_WEIGHTS_PATH,
    _device
)

def format_bar(pct: float, width: int = 28, fill_char: str = "#") -> str:
    filled = int(round((pct / 100.0) * width))
    return f"[{fill_char * filled}{'-' * (width - filled)}] {pct:5.1f}%"

def test_document(image_path: Path):
    if not image_path.exists():
        print(f"[ERROR] File not found: {image_path}")
        return

    print("\n" + "=" * 70)
    print(f"  EXAMINING: {image_path.name}")
    print("=" * 70)

    t0 = time.perf_counter()
    result = run_deep_learning_inference(image_path, case_uid=f"CLI-{image_path.stem[:8].upper()}")
    elapsed = (time.perf_counter() - t0) * 1000.0

    probs = result["probabilities"]
    pred = result["predicted_label"]
    conf = result["confidence"]

    print(f"\n  [RESULT] PREDICTED OUTCOME:  {pred}")
    print(f"  [RESULT] CONFIDENCE SCORE:   {conf}%\n")

    print("  SOFTMAX PROBABILITY BREAKDOWN:")
    print(f"    - Genuine        {format_bar(probs['genuine'])}")
    print(f"    - Forged/Spliced {format_bar(probs['forged'])}")
    print(f"    - Inconclusive   {format_bar(probs['inconclusive'])}")

    print(f"\n  NEURAL METRICS:")
    print(f"    - Model:               {result['model_name']}")
    print(f"    - Framework / Device:  {result['framework']} on {result['device']}")
    print(f"    - Inference Latency:   {elapsed:.1f} ms")
    print(f"    - Tamper Activation:   Max: {result['tamper_activation_max']} | Mean: {result['tamper_activation_mean']}")
    print(f"    - Heatmap Saved To:    storage/uploads/{result['heatmap_file']}")
    print("=" * 70)

def main():
    print("*" * 70)
    print("  INTELLIGENT DOCUMENT AUTHENTICATION SYSTEM -- RUNNING MODEL")
    print("  Dual-Stream ResNet + ELA Cross-Attention (1,139,845 parameters)")
    print("*" * 70)

    summary = get_model_summary()
    print(f"  - Weights Loaded:   {summary['weights_loaded']} ({summary['weights_path']})")
    print(f"  - Compute Device:   {summary['device'].upper()}")
    print(f"  - Total Parameters: {summary['total_parameters']:,}")

    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1])
        test_document(target_path)
    else:
        print("\n  No file specified. Running model on 3 standard benchmark samples:")
        samples = [
            Path("app/static/samples/sample1_verified_degree.png"),
            Path("app/static/samples/sample2_altered_identity.png"),
            Path("app/static/samples/sample4_blurry_scan.png")
        ]
        for s in samples:
            if s.exists():
                test_document(s)
            else:
                print(f"  [Notice] Sample {s} not found.")

if __name__ == "__main__":
    main()
