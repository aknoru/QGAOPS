"""
LIVE HAND GA ENGINE — scripts/extract_features.py
Feature extraction for LeapGestRecog hand-expression dataset.

[IMPLEMENTED]
1. Runs MediaPipe hand-landmark detector on every dataset image.
2. Extracts normalized geometric features (x,y,z, lengths, joint angles,
   openness, palm normal, pinch distance, inter-finger distances).
3. Extracts lightweight image features (HOG / downsampled pixels) as baseline.
4. Records detection failures honestly without creating fake landmarks.
5. Saves extracted features and detection failure statistics.
"""
from __future__ import annotations

import json
import os
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hand_detection.detector import HandDetector
from hand_detection.landmarks import HandGeometryExtractor, HandGeometry
from mapping.dataset_classes import CLASS_NAMES, FOLDER_TO_NAME, NAME_TO_ID


def extract_geometric_features(geom: HandGeometry, raw_lms: np.ndarray) -> np.ndarray:
    """Extract a 1D normalized geometric feature vector from HandGeometry and landmarks."""
    # Palm scale: distance from wrist to middle MCP or wrist to palm center
    scale = max(float(np.linalg.norm(geom.palm_center - geom.wrist)), 1e-4)
    wrist = geom.wrist

    # 1. 21 relative landmark coordinates (normalized by scale)
    rel_lms = (raw_lms - wrist) / scale
    coords_feat = rel_lms.flatten()  # 63

    # 2. Finger lengths
    finger_names = ["thumb", "index", "middle", "ring", "pinky"]
    flens = np.array([geom.finger_lengths.get(f, 0.0) / scale for f in finger_names], dtype=np.float32)

    # 3. Wrist to tip distances
    w2t = np.array([geom.wrist_to_tip_dists.get(f, 0.0) / scale for f in finger_names], dtype=np.float32)

    # 4. Fingertip to palm distances
    p2t = np.array([geom.palm_to_tip_dists.get(f, 0.0) / scale for f in finger_names], dtype=np.float32)

    # 5. Mean joint angles per finger
    j_angles = []
    for f in finger_names:
        angles = geom.joint_angles.get(f, [])
        j_angles.append(float(np.mean(angles)) if angles else 0.0)
    j_angles = np.array(j_angles, dtype=np.float32)

    # 6. Inter-fingertip pairwise distances (10 pairs)
    inter_dists = []
    pairs = [
        ("thumb", "index"), ("thumb", "middle"), ("thumb", "ring"), ("thumb", "pinky"),
        ("index", "middle"), ("index", "ring"), ("index", "pinky"),
        ("middle", "ring"), ("middle", "pinky"),
        ("ring", "pinky"),
    ]
    for p in pairs:
        inter_dists.append(geom.fingertip_distances.get(p, 0.0) / scale)
    inter_dists = np.array(inter_dists, dtype=np.float32)

    # 7. Inter-finger adjacent angles (4 pairs)
    adj_pairs = [("thumb", "index"), ("index", "middle"), ("middle", "ring"), ("ring", "pinky")]
    adj_angles = np.array([geom.inter_finger_angles.get(p, 0.0) for p in adj_pairs], dtype=np.float32)

    # 8. Palm normal
    p_norm = geom.palm_normal.astype(np.float32)  # 3

    # 9. Pinch distance
    pinch_dist = np.array([geom.fingertip_distances.get(("thumb", "index"), 1.0) / scale], dtype=np.float32)

    # 10. Hand openness
    openness = np.array([np.mean(w2t)], dtype=np.float32)

    # 11. Finger extension ratios
    ext_ratios = np.array([
        (geom.wrist_to_tip_dists.get(f, 0.0) / (geom.finger_lengths.get(f, 1.0) + 1e-6))
        for f in finger_names
    ], dtype=np.float32)

    return np.concatenate([
        coords_feat, flens, w2t, p2t, j_angles,
        inter_dists, adj_angles, p_norm, pinch_dist, openness, ext_ratios
    ])


def extract_image_features(gray_img: np.ndarray, target_size: Tuple[int, int] = (64, 64)) -> np.ndarray:
    """Extract lightweight image baseline features using downsampling and HOG."""
    resized = cv2.resize(gray_img, target_size, interpolation=cv2.INTER_AREA)

    # Normalize image to [0, 1]
    norm_pixels = (resized.astype(np.float32) / 255.0).flatten()

    # Compute lightweight Sobel gradients (HOG-like proxy)
    gx = cv2.Sobel(resized, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(resized, cv2.CV_32F, 0, 1, ksize=3)
    mag, ang = cv2.cartToPolar(gx, gy)

    # 8-bin orientation histogram per 16x16 block (4x4 = 16 blocks * 8 bins = 128 features)
    hist_list = []
    cell_size = 16
    for i in range(0, target_size[0], cell_size):
        for j in range(0, target_size[1], cell_size):
            cell_mag = mag[i:i+cell_size, j:j+cell_size]
            cell_ang = ang[i:i+cell_size, j:j+cell_size]
            hist, _ = np.histogram(cell_ang, bins=8, range=(0, 2*np.pi), weights=cell_mag)
            norm = np.linalg.norm(hist) + 1e-6
            hist_list.append(hist / norm)

    hog_feat = np.concatenate(hist_list).astype(np.float32)

    # Combined downsampled pixels (16x16) + HOG
    small_pixels = cv2.resize(resized, (16, 16), interpolation=cv2.INTER_AREA).flatten().astype(np.float32) / 255.0

    return np.concatenate([small_pixels, hog_feat])


def process_dataset(
    dataset_dir: str = "LeapGestRecog_1/LeapGestRecog_1",
    output_dir: str = "dataset/features",
) -> Dict[str, Any]:
    print("\n==================================================")
    print("  FEATURE EXTRACTION PIPELINE")
    print("==================================================")
    print(f"Dataset: {dataset_dir}")
    print(f"Output:  {output_dir}")

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("results", exist_ok=True)

    detector = HandDetector(min_detection_conf=0.15, min_tracking_conf=0.15)
    extractor = HandGeometryExtractor()

    landmark_features = []
    landmark_labels = []
    landmark_metadata = []

    image_features = []
    image_labels = []
    image_metadata = []

    detection_stats: Dict[str, Dict[str, int]] = {}

    t0 = time.perf_counter()

    for folder_name, class_name in FOLDER_TO_NAME.items():
        class_id = NAME_TO_ID[class_name]
        class_dir = os.path.join(dataset_dir, folder_name)
        if not os.path.exists(class_dir):
            print(f"  [WARN] Skipping missing directory: {class_dir}")
            continue

        image_files = sorted([
            f for f in os.listdir(class_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ])

        total_class_images = len(image_files)
        detected_count = 0

        for img_name in image_files:
            img_path = os.path.join(class_dir, img_name)
            gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if gray is None:
                continue

            # 1. Image features (always available for every sample)
            img_feat = extract_image_features(gray)
            image_features.append(img_feat)
            image_labels.append(class_id)
            image_metadata.append({"path": img_path, "class": class_name, "id": class_id})

            # 2. Hand landmark detection
            bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            hands = detector.detect(bgr)

            if hands:
                detected_count += 1
                hand = hands[0]
                raw_lms = hand.to_array()
                geom = extractor.extract(raw_lms, raw_lms, hand.confidence, hand.handedness, frame_index=0)
                geo_feat = extract_geometric_features(geom, raw_lms)

                landmark_features.append(geo_feat)
                landmark_labels.append(class_id)
                landmark_metadata.append({
                    "path": img_path,
                    "class": class_name,
                    "id": class_id,
                    "confidence": hand.confidence,
                })

        detection_stats[class_name] = {
            "total": total_class_images,
            "detected": detected_count,
            "failed": total_class_images - detected_count,
            "success_rate_pct": round((detected_count / total_class_images) * 100.0, 1) if total_class_images else 0.0,
        }

        print(f"  {class_name:<12} | Detected: {detected_count}/{total_class_images} ({detection_stats[class_name]['success_rate_pct']}%)")

    detector.close()
    elapsed = time.perf_counter() - t0

    # Convert to arrays
    X_img = np.array(image_features, dtype=np.float32)
    y_img = np.array(image_labels, dtype=np.int64)

    X_lm = np.array(landmark_features, dtype=np.float32) if landmark_features else np.zeros((0, 107), dtype=np.float32)
    y_lm = np.array(landmark_labels, dtype=np.int64) if landmark_labels else np.zeros((0,), dtype=np.int64)

    # Save features
    out_npz = os.path.join(output_dir, "extracted_features.npz")
    np.savez_compressed(
        out_npz,
        X_image=X_img,
        y_image=y_img,
        X_landmark=X_lm,
        y_landmark=y_lm,
    )

    total_images_processed = len(y_img)
    total_detected = len(y_lm)
    overall_detection_rate = (total_detected / total_images_processed * 100.0) if total_images_processed else 0.0

    report = {
        "dataset_dir": dataset_dir,
        "total_images_processed": total_images_processed,
        "landmark_samples_extracted": total_detected,
        "overall_detection_rate_pct": round(overall_detection_rate, 2),
        "overall_failure_rate_pct": round(100.0 - overall_detection_rate, 2),
        "image_feature_dim": int(X_img.shape[1]) if len(X_img) else 0,
        "landmark_feature_dim": int(X_lm.shape[1]) if len(X_lm) else 0,
        "detection_by_class": detection_stats,
        "extraction_time_s": round(elapsed, 2),
    }

    report_path = os.path.join("results", "feature_extraction_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n[DONE] Feature extraction complete in {elapsed:.2f}s")
    print(f"  Landmark feature shape: {X_lm.shape}")
    print(f"  Image feature shape:    {X_img.shape}")
    print(f"  Detection Success:      {total_detected}/{total_images_processed} ({overall_detection_rate:.1f}%)")
    print(f"  Saved features:         {out_npz}")
    print(f"  Saved report:           {report_path}")

    return report


if __name__ == "__main__":
    process_dataset()
