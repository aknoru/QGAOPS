# Live Hand Geometric Algebra Engine
### QGAOPS-QGPU Software Demonstrator & Python Golden Model

> **[SOFTWARE DEMONSTRATOR]** This is the interactive Python golden model for the
> **QGAOPS-QGPU** research project: *Design and FPGA Implementation of a
> Memory-Aware Quantum-Geometric Algebra Processing Unit for Edge Computing*.

---

## What Does It Do?

This application uses your laptop webcam to detect a **live human hand**,
converts its geometry into **Geometric Algebra (GA) multivectors**, and
performs real-time algebraic operations on them — **demonstrating in software
what the QGAOPS-QGPU FPGA accelerator will eventually compute in hardware**.

```
WEBCAM → HAND DETECTION → LANDMARK EXTRACTION → HAND GEOMETRY
  → GA ENCODING → OPERATION ANALYSIS → SCHEDULING → SHARED GA ENGINE
  → RESULT → VISUALIZATION
```

---

## Quick Start

```bash
cd hand_ga_engine

# Install dependencies
pip install -r requirements.txt

# Run live demo (webcam required)
python main.py

# Run without webcam (synthetic mode)
python main.py --no-webcam

# Benchmark mode
python main.py --benchmark

# FIX16 mode (Q1.14 fixed-point comparison)
python main.py --fixed

# Generate golden vectors (for RTL verification)
python main.py --generate-golden

# Run with Computer Vision Control (Mouse Profile)
python main.py --control mouse

# Run with Hands-free Presentation Control
python main.py --control presentation

# Run with GA Rotor 3D Virtual Object Manipulation
python main.py --control object3d

# Launch PySide6 Engineering Dashboard (10 Functional Tabs including Computer Control)
python main.py --gui

# Profile per-stage latency
python main.py --profile

# Record hand landmarks
python main.py --record

# Replay from recording
python main.py --replay recording.json

# Deterministic experiment
python main.py --experiment
```

## Run Tests

```bash
cd hand_ga_engine
pytest tests/ -v
```

---

## Architecture

```
hand_ga_engine/
├── main.py                    # Entry point — all CLI modes
├── config/config.py           # Centralized configuration
│
├── ga/                        # Geometric Algebra engine [IMPLEMENTED]
│   ├── basis.py               #   Bitmask basis elements, grade, sign
│   ├── metric.py              #   Metric tensor G(p,q,r)
│   ├── multivector.py         #   8-element G3 multivector
│   ├── geometric_product.py   #   GP, wedge, inner, dot, cross
│   ├── operations.py          #   Reverse, dual, commutator, norm
│   ├── rotor.py               #   Rotor construction, sandwich product
│   └── ir.py                  #   QGAOPS IR (JSON + binary)
│
├── fixed_point/               # Q1.14 FIX16 software model [IMPLEMENTED]
│   └── fix16.py
│
├── backend/                   # Hardware abstraction layer
│   ├── python_backend.py      #   [IMPLEMENTED] NumPy execution
│   └── fpga_backend.py        #   [PROPOSED] FPGA stub only
│
├── engine/                    # Algebra Engine + Scheduler
│   ├── algebra_engine.py      #   [IMPLEMENTED] Unified dispatch
│   └── operation_scheduler.py #   [IMPLEMENTED] DAG + memory model
│
├── hand_detection/            # Hand tracking [IMPLEMENTED]
│   ├── detector.py            #   MediaPipe wrapper + fallback
│   ├── landmarks.py           #   Smoother + HandGeometry
│   └── gesture.py             #   Static pose recognizer (14 poses)
│
├── mapping/                   # Landmark → GA [IMPLEMENTED]
│   └── hand_to_ga.py
│
├── expression/                # Dynamic expression recognition [IMPLEMENTED]
│   ├── dynamic_recognizer.py  #   Temporal sliding-window
│   ├── state_machine.py       #   7-state FSM (IDLE→COOLDOWN)
│   └── expression_to_ga.py   #   Expression → GA operation → IR
│
├── control/                   # Computer vision gesture control layer [IMPLEMENTED]
│   ├── safety.py              #   Opt-in, F12 emergency cut-off, debounce, confirmation
│   ├── command_mapper.py      #   YAML profile loader & dynamic profile switcher
│   ├── mouse_controller.py    #   Smoothed cursor, dead-zone, pinch click/drag
│   ├── scroll_controller.py   #   Rate-limited discrete scroll bursts
│   ├── keyboard_controller.py #   Whitelisted key dispatcher (zero arbitrary execution)
│   ├── application_controller.py # Presentation slideshow & media controllers
│   ├── object3d.py            #   GA rotor sandwich product 3D virtual object
│   └── controller.py          #   Main coordinator, telemetry & rotating CSV logger
│
├── profiles/                  # Configurable YAML gesture control profiles
│   ├── mouse.yaml             #   Cursor navigation, pinch clicks & drag, right click
│   ├── presentation.yaml      #   Slideshow next/prev, start (F5), escape
│   ├── media.yaml             #   Play/pause, skip, stop
│   └── object3d.yaml          #   GA rotor rotation (CW/CCW), zoom, pan, reset
│
├── gui/                       # PySide6 Engineering Dashboard [IMPLEMENTED]
│   └── dashboard_window.py    #   10 Functional Tabs including Tab 10 "COMPUTER CONTROL"
│
├── visualization/             # Visualization & HUD [IMPLEMENTED]
│   ├── webcam_view.py         #   OpenCV overlay
│   ├── control_overlay.py     #   Transparent Control HUD overlay (F12 reminder)
│   ├── vector_view.py         #   Matplotlib 3D
│   └── dashboard.py           #   Composite layout
│
└── tests/                     # Unit tests (166 tests passing, mock backend) [IMPLEMENTED]
    └── test_control.py        #   Control safety, profiles, mouse, keyboard & GA rotor tests
```

---

## Supported GA Operations

| Operation | Key | Description |
|:---|:---|:---|
| Geometric Product | `G` | `a*b = a·b + a∧b` |
| Wedge Product | `W` | `a∧b` — oriented plane/area |
| Dot Product | `D` | `a·b` — scalar alignment |
| Inner Product | (auto) | Grade-lowering product |
| Reverse | (auto) | `~A` — grade-dependent sign |
| Rotor | `R` | `R = cos(θ/2) - sin(θ/2)·B` |
| Sandwich Product | `S` | `R*v*~R` — rotation |
| Dual | (auto) | `A* = A·I⁻¹` |
| Commutator | (auto) | `[A,B] = (AB-BA)/2` |
| Norm | (auto) | `||A||` |

---

## Recognized Hand Gestures

| Pose | GA Operation Triggered |
|:---|:---|
| OPEN_PALM | All finger direction vectors |
| FIST | Contraction magnitudes |
| THUMBS_UP | Thumb direction vector |
| INDEX_POINT | Index pointing vector |
| TWO_FINGER | `v_index ∧ v_middle` (wedge) |
| THREE_FINGER | `v_i * v_m * v_r` (triple GP) |
| PINCH | `||thumb_tip - index_tip||` (distance) |
| OK_SIGN | `v_index · v_middle` (dot product) |
| ROCK_SIGN | `v_index ∧ v_pinky` (wedge) |
| ROTATE_CW | Rotor sandwich product |
| SWIPE_LEFT | Displacement vector |
| SWIPE_RIGHT | Displacement vector |

---

## Keyboard Controls

| Key | Action |
|:---|:---|
| `Q` | Quit |
| `M` | Next mode |
| `G` | Geometric Product mode |
| `D` | Dot Product mode |
| `W` | Wedge Product mode |
| `R` | Rotor mode |
| `S` | Sandwich Product mode |
| `F` | Toggle FIX16 mode |
| `B` | Run benchmark |
| `V` | Toggle 3D vector view |
| `H` | Help |

---

## FIX16 Mode

`python main.py --fixed`

Compares **FLOAT32** vs **Q1.14 FIX16** results for every geometric product.
Displays max/mean/RMS absolute error in the dashboard.

**[SOFTWARE MODEL]** — simulates the Q1.14 fixed-point datapath that will
be implemented in the QGAOPS-QGPU FPGA hardware.

---

## Golden Vectors

`python main.py --generate-golden`

Generates deterministic JSON test vectors in `golden/hand_ga_golden.json`:
- GA product pairs (FLOAT32 + FIX16 + error)
- Rotor sandwich products for multiple axes and angles
- Synthetic hand landmark → GA mapping vectors

**Use case:** RTL testbench inputs/expected outputs for FPGA verification.

---

## FPGA Future Integration

| Status | Component |
|:---|:---|
| **[IMPLEMENTED]** | Python GA engine (golden model) |
| **[IMPLEMENTED]** | FIX16 Q1.14 software model |
| **[IMPLEMENTED]** | QGAOPS IR (JSON + binary packets) |
| **[IMPLEMENTED]** | Operation scheduler + memory model |
| **[PROPOSED]** | AXI-Lite control interface |
| **[PROPOSED]** | AXI DMA operand transfer |
| **[PROPOSED]** | BRAM scratchpad |
| **[NOT IMPLEMENTED]** | Actual Zynq/ZedBoard execution |
| **[NOT IMPLEMENTED]** | Vivado synthesis |

---

## Limitations

See [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md) for full list.

Key limitations:
1. MediaPipe `z` coordinate is relative depth only (not metric millimeters).
2. Matplotlib 3D view limits FPS to ~15-20 fps (update every 3 frames).
3. FIX16 Q1.14 range is `[-2.0, +1.9999]` — unit vectors fit but large coordinates do not.
4. No actual FPGA is connected. `fpga_backend.py` is a stub.
5. Gesture recognition is rule-based, not ML-based. Edge cases may produce `UNKNOWN`.

---

## Citation / Research Context

This software demonstrator supports the research project:

> **QGAOPS-QGPU: Design and FPGA Implementation of a Memory-Aware
> Quantum-Geometric Algebra Processing Unit for Edge Computing**

All results from this software are labelled `[IMPLEMENTED]` (software-validated).
No FPGA performance numbers are fabricated.
