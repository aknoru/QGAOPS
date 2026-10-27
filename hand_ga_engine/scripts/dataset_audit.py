"""
LIVE HAND GA ENGINE — scripts/dataset_audit.py
Inspect and audit the Kaggle LeapGestRecog hand-expression dataset.

[IMPLEMENTED] Checks total images, image sizes, color channels, corrupted files,
              duplicates via SHA-256 hash, and class distribution.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import cv2
import numpy as np

CLASS_MAPPING = {
    "01_palm": "PALM",
    "02_l": "L_GESTURE",
    "03_fist": "FIST",
    "05_thumb": "THUMB",
    "06_index": "INDEX",
    "07_ok": "OK",
}


def audit_dataset(dataset_dir: str = "LeapGestRecog_1/LeapGestRecog_1") -> Dict[str, Any]:
    print(f"\n==================================================")
    print(f"  DATASET AUDIT: {dataset_dir}")
    print(f"==================================================")

    if not os.path.exists(dataset_dir):
        print(f"[ERROR] Dataset directory not found: {dataset_dir}")
        sys.exit(1)

    classes_found = {}
    corrupted_files = []
    hash_to_path = {}
    duplicates = []
    dimensions_set = set()
    channels_set = set()
    total_images = 0

    for folder_name, class_name in CLASS_MAPPING.items():
        class_path = os.path.join(dataset_dir, folder_name)
        if not os.path.exists(class_path):
            print(f"  [WARN] Missing folder: {folder_name}")
            classes_found[class_name] = {"count": 0, "status": "MISSING"}
            continue

        image_files = [
            f for f in os.listdir(class_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))
        ]
        classes_found[class_name] = {"count": len(image_files), "folder": folder_name}

        for img_file in image_files:
            total_images += 1
            full_path = os.path.join(class_path, img_file)

            # Read image
            img = cv2.imread(full_path, cv2.IMREAD_UNCHANGED)
            if img is None:
                corrupted_files.append({"path": full_path, "error": "cv2.imread failed"})
                continue

            # Shape and channels
            if len(img.shape) == 2:
                h, w = img.shape
                c = 1
            else:
                h, w, c = img.shape

            dimensions_set.add(f"{w}x{h}")
            channels_set.add(c)

            # Duplicate check via SHA-256
            try:
                with open(full_path, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                if file_hash in hash_to_path:
                    duplicates.append({
                        "original": hash_to_path[file_hash],
                        "duplicate": full_path,
                    })
                else:
                    hash_to_path[file_hash] = full_path
            except Exception as e:
                corrupted_files.append({"path": full_path, "error": str(e)})

    report = {
        "dataset_path": dataset_dir,
        "total_images": total_images,
        "classes": classes_found,
        "class_distribution": {k: v["count"] for k, v in classes_found.items()},
        "dimensions": list(dimensions_set),
        "channels": list(channels_set),
        "corrupted_count": len(corrupted_files),
        "corrupted_files": corrupted_files,
        "duplicate_count": len(duplicates),
        "duplicates": duplicates[:10],  # show first 10
        "audit_status": "SUCCESS" if len(corrupted_files) == 0 else "CORRUPTED_DETECTED",
    }

    # Print summary
    print(f"\nAudit Summary:")
    print(f"  Total Images:    {report['total_images']}")
    print(f"  Classes:         {len(classes_found)}")
    for cname, info in classes_found.items():
        print(f"    - {cname:<12} ({info.get('folder', 'N/A')}): {info['count']} images")
    print(f"  Image Dimensions: {', '.join(report['dimensions'])}")
    print(f"  Color Channels:   {report['channels']} (1=Grayscale/IR, 3=BGR)")
    print(f"  Corrupted Files:  {report['corrupted_count']}")
    print(f"  Duplicate Files:  {report['duplicate_count']}")
    print(f"  Audit Status:     {report['audit_status']}")

    # Save to results/dataset_report.json
    os.makedirs("results", exist_ok=True)
    out_path = os.path.join("results", "dataset_report.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n[SAVED] Dataset report written to {out_path}\n")

    return report


if __name__ == "__main__":
    audit_dataset()
