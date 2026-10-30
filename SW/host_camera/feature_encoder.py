#!/usr/bin/env python3
"""
feature_encoder.py - Geometric Algebra Landmark Feature Encoder
Maps 21 3D hand landmarks into Cl(3,0) multivectors and Q16.16 fixed-point format.
"""

import numpy as np
from SW.reference.ga_reference import Cl30Multivector, to_q16, from_q16

# MediaPipe Hand Landmark Indices
WRIST = 0
THUMB_CMC = 1; THUMB_MCP = 2; THUMB_IP = 3; THUMB_TIP = 4
INDEX_MCP = 5; INDEX_PIP = 6; INDEX_DIP = 7; INDEX_TIP = 8
MIDDLE_MCP = 9; MIDDLE_PIP = 10; MIDDLE_DIP = 11; MIDDLE_TIP = 12
RING_MCP = 13; RING_PIP = 14; RING_DIP = 15; RING_TIP = 16
PINKY_MCP = 17; PINKY_PIP = 18; PINKY_DIP = 19; PINKY_TIP = 20

def normalize_landmarks(landmarks):
    """
    Translates landmarks so wrist is at origin (0,0,0) and scales by palm size.
    """
    pts = np.array([[lm.x, lm.y, lm.z] for lm in landmarks], dtype=np.float64)
    wrist = pts[WRIST]
    pts = pts - wrist
    
    # Scale by distance from wrist to middle MCP
    scale = np.linalg.norm(pts[MIDDLE_MCP])
    if scale > 1e-4:
        pts = pts / scale
    return pts

def encode_hand_multivectors(norm_pts):
    """
    Constructs geometric algebra multivectors from normalized landmarks:
      1. Palm Bivector B_palm = v_index_mcp ^ v_pinky_mcp (orientation of palm plane)
      2. Finger vectors v_thumb, v_index, v_middle, v_ring, v_pinky
      3. Rotor R representing palm orientation relative to canonical XY plane
    """
    v_index_mcp = norm_pts[INDEX_MCP]
    v_pinky_mcp = norm_pts[PINKY_MCP]
    v_middle_mcp = norm_pts[MIDDLE_MCP]

    # Basis vectors: e1=(1,0,0), e2=(0,1,0), e3=(0,0,1)
    mv_v1 = Cl30Multivector([0, v_index_mcp[0], v_index_mcp[1], v_index_mcp[2], 0, 0, 0, 0])
    mv_v2 = Cl30Multivector([0, v_pinky_mcp[0], v_pinky_mcp[1], v_pinky_mcp[2], 0, 0, 0, 0])

    # Palm plane bivector: B = v1 ^ v2
    b_palm = mv_v1.wedge_product(mv_v2)

    # Finger vectors (tip - mcp)
    finger_mvs = []
    tips = [THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]
    mcps = [THUMB_MCP, INDEX_MCP, MIDDLE_MCP, RING_MCP, PINKY_MCP]
    for tip_idx, mcp_idx in zip(tips, mcps):
        vec = norm_pts[tip_idx] - norm_pts[mcp_idx]
        mv = Cl30Multivector([0, vec[0], vec[1], vec[2], 0, 0, 0, 0])
        finger_mvs.append(mv)

    # Rotor R = cos(theta/2) - sin(theta/2)*B_norm
    b_norm_sq = b_palm.geometric_product(b_palm.reversion()).grade_project(0).to_floats()[0]
    b_len = np.sqrt(max(0.0, b_norm_sq))
    
    if b_len > 1e-4:
        # Construct normalized rotor
        theta = np.arctan2(b_len, max(1e-4, v_middle_mcp[2]))
        half_th = theta * 0.5
        cos_half = np.cos(half_th)
        sin_half = np.sin(half_th) / b_len
        r_blades = [
            cos_half, 0, 0, 0,
            -sin_half * from_q16(b_palm.blades[4]),
            -sin_half * from_q16(b_palm.blades[5]),
            -sin_half * from_q16(b_palm.blades[6]),
            0
        ]
        rotor = Cl30Multivector(r_blades)
    else:
        rotor = Cl30Multivector([1.0, 0, 0, 0, 0, 0, 0, 0])

    return {
        "b_palm": b_palm,
        "rotor": rotor,
        "fingers": finger_mvs
    }
