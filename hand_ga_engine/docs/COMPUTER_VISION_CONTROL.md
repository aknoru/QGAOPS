# Computer Vision Gesture Control System — Architecture & Specification

## 1. Executive Summary

Phase 5 upgrades the **QGAOPS Live Hand Geometric Algebra Engine** into an interactive real-time **Computer Vision Gesture Control Interface**.
The system operates a dual-stream architecture:
1. **Geometric Algebra Pipeline:** Processes 21 landmarks into multivectors $\mathcal{G}_3$, computes GA operations (wedge, dot, geometric product, rotors, sandwich products), and schedules QGAOPS IR instructions for future FPGA execution.
2. **Computer Vision Control Pipeline:** Evaluates the detected 13 static hand poses and 14 dynamic motion expressions, routes them through a configurable profile mapper, enforces strict multi-layered safety interlocks, and dispatches whitelisted OS input actions (mouse, keyboard, presentations, media, or GA-driven 3D virtual object manipulation).

```
                        CAMERA FRAME
                             │
                     HAND DETECTION (21 3D Landmarks)
                             │
           ┌─────────────────┴─────────────────┐
           ▼                                   ▼
   [GA MATHEMATICAL PIPELINE]          [GESTURE CONTROL PIPELINE]
           │                                   │
   Multivectors in G(3,0,0)            Pose & Motion Classification
           │                                   │
   GA Operation Computation            Temporal Smoothing (Consensus)
   (Dot, Wedge, GP, Rotor)                     │
           │                           Safety Manager & Debounce
   QGAOPS IR Instruction                       │
   (Hardware Acceleration Trace)       Command Mapper (Active Profile)
                                               │
                                       OS Action Execution / 3D Rotor
```

> [!NOTE]
> **Honest Scientific Metric Classification:**
> - Computer Vision & Control Actions: `[MEASURED SOFTWARE]`
> - Memory Fabric & Scratchpad Hierarchy: `[SOFTWARE MODEL]`
> - FPGA Physical Bitstream & Registers: `[N/A — FPGA NOT CONNECTED]`

---

## 2. Safety Model & Interlocks

Security and physical safety are primary design requirements. Operating system inputs can disrupt user workflows if triggered accidentally.

### 2.1 Opt-in by Default (`CONTROL = DISABLED`)
When the application starts, the control subsystem is initialized in the `ControlState.DISABLED` state. No physical mouse movements or keystrokes occur unless explicitly enabled:
- **GUI:** User must click the **ENABLE CONTROL** button in Tab 10 ("10. COMPUTER CONTROL").
- **CLI:** User must explicitly pass the `--control [profile]` flag.

### 2.2 Emergency Cut-Off (`F12` / Emergency Button)
- Pressing `F12` anywhere in the dashboard window, in the terminal, or clicking **EMERGENCY STOP (F12)** instantly halts all control dispatching and transitions the state machine to `ControlState.EMERGENCY_STOPPED`.
- All ongoing mouse drags are released immediately (`mouse_up("left")`).
- Pending confirmations are purged.
- Resuming requires explicitly clicking **Reset Emergency** followed by **ENABLE CONTROL**.

### 2.3 Strict Command Whitelisting
- Arbitrary shell commands, subprocesses, or arbitrary key combinations are strictly prohibited.
- `KeyboardController.ALLOWED_KEYS` only permits benign navigation keys:
  `{"left", "right", "up", "down", "pageup", "pagedown", "home", "end", "space", "enter", "escape", "tab", "f5", "b", "w", "playpause", "prevtrack", "nexttrack", "stop", "volumeup", "volumedown", "volumemute"}`.

### 2.4 Confirmation Workflow (`OK_SIGN`)
- High-impact commands (e.g. `START_PRESENTATION`, `MEDIA_STOP`) do not fire immediately.
- The safety layer places the action into a `PendingConfirmation` buffer with a 4.0-second expiry timer.
- The user must form an `OK_SIGN` gesture within the time window to confirm execution.

### 2.5 Debounce & Rate Limiting
- **Continuous Gestures** (`CURSOR_MOVE`, `MOUSE_DRAG`, `OBJECT_TRANSLATE`): Bypass discrete debounce timers to ensure fluid 60 FPS tracking.
- **Discrete Gestures** (`RIGHT_CLICK`, `SWIPE_LEFT`, `SWIPE_RIGHT`, `PINCH_START`): Strictly rate-limited (cooldown 250ms to 800ms) to prevent multi-triggering.

---

## 3. Profiles & Command Mapping

Profiles are defined using YAML files located in `profiles/`:

### 3.1 Mouse Profile (`profiles/mouse.yaml`)
| Trigger Gesture | Command | Description | Safety / Rate Limit |
|---|---|---|---|
| `INDEX_POINT` | `CURSOR_MOVE` | Moves OS cursor to index fingertip coordinates | Continuous (EMA smoothed) |
| `PINCH_START` | `MOUSE_DOWN` | Left mouse button down (click or drag start) | Cooldown: 250ms |
| `PINCH_HOLD` | `MOUSE_DRAG` | Moves cursor while holding left mouse button | Continuous |
| `PINCH_RELEASE` | `MOUSE_UP` | Left mouse button release | Rising edge trigger |
| `TWO_FINGER` | `RIGHT_CLICK` | Right click context menu | Cooldown: 400ms |
| `SWIPE_UP` | `SCROLL_UP` | Scroll up discrete burst | Cooldown: 200ms |
| `SWIPE_DOWN` | `SCROLL_DOWN` | Scroll down discrete burst | Cooldown: 200ms |

### 3.2 Presentation Profile (`profiles/presentation.yaml`)
| Trigger Gesture | Command | Dispatched Key | Description |
|---|---|---|---|
| `SWIPE_RIGHT` | `NEXT_SLIDE` | `Right Arrow` | Next slide / advance animation |
| `SWIPE_LEFT` | `PREV_SLIDE` | `Left Arrow` | Previous slide |
| `OPEN_PALM` | `START_PRESENTATION` | `F5` | Start slideshow (Requires `OK_SIGN` confirm) |
| `FIST` | `ESCAPE_PRESENTATION` | `Escape` | Exit slideshow |
| `INDEX_POINT` | `CURSOR_MOVE` | Cursor coordinates | Laser pointer spotlight navigation |

### 3.3 Media Profile (`profiles/media.yaml`)
*(Disabled by default in settings)*
| Trigger Gesture | Command | Dispatched Key | Description |
|---|---|---|---|
| `THUMBS_UP` | `PLAY_PAUSE` | `Space` / `PlayPause` | Toggle media playback |
| `SWIPE_RIGHT` | `MEDIA_NEXT` | `NextTrack` | Skip to next track |
| `SWIPE_LEFT` | `MEDIA_PREVIOUS` | `PrevTrack` | Return to previous track |
| `FIST` | `MEDIA_STOP` | `Stop` | Stop playback (Requires `OK_SIGN` confirm) |

### 3.4 GA-Driven Virtual 3D Object Profile (`profiles/object3d.yaml`)
Controls a 3D wireframe cube represented as Clifford algebra grade-1 multivectors:
| Trigger Gesture | Command | GA Operation | Mathematical Formula |
|---|---|---|---|
| `ROTATE_CLOCKWISE` | `OBJECT_ROTATE_CW` | Rotor sandwich | $v' = R v \widetilde{R},\quad R = e^{-\frac{\theta}{2} B}$ |
| `ROTATE_COUNTERCLOCKWISE` | `OBJECT_ROTATE_CCW` | Reverse rotor sandwich | $v' = \widetilde{R} v R$ |
| `HAND_APPROACH` | `OBJECT_ZOOM_IN` | Dilation | $v' = \lambda v,\quad \lambda = 1.10$ |
| `HAND_RETRACT` | `OBJECT_ZOOM_OUT` | Contraction | $v' = \lambda v,\quad \lambda = 0.90$ |
| `SWIPE_LEFT` / `RIGHT` | `OBJECT_PAN` | Translation | $v' = v + \mathbf{t}$ |
| `FIST` | `OBJECT_RESET` | Identity Reset | Restore canonical geometry |

---

## 4. GA Rotor 3D Object Manipulation Model

The `Virtual3DObject` class demonstrates the direct connection between real-time computer vision control and Clifford Geometric Algebra:

1. **Vertex Representation:**
   The 8 cube vertices $\mathbf{v}_i \in \mathcal{G}_1$ are stored as 8-component multivectors:
   $$\mathbf{v} = v_x \mathbf{e}_0 + v_y \mathbf{e}_1 + v_z \mathbf{e}_2$$

2. **Rotor Construction:**
   For rotation by angle $\theta$ about unit axis $\hat{\mathbf{n}}$ with dual unit bivector $B = \hat{\mathbf{n}}^*$:
   $$R = \cos\left(\frac{\theta}{2}\right) - \sin\left(\frac{\theta}{2}\right) B$$

3. **Sandwich Product:**
   Every vertex is transformed using the GA sandwich product:
   $$\mathbf{v}' = R \mathbf{v} \widetilde{R}$$
   This preserves both the grade ($\mathbf{v}' \in \mathcal{G}_1$) and the metric norm ($|\mathbf{v}'| = |\mathbf{v}|$).

4. **Live Transformation Trace:**
   The mathematical trace records:
   - Original vector $\mathbf{v}$
   - Rotor $R$
   - Reverse rotor $\widetilde{R}$
   - Transformed vector $\mathbf{v}'$
   - Rotor norm $|R| \approx 1.0000$

---

## 5. Latency & Telemetry Analysis

Latency tracking isolates pipeline stages with microsecond precision:
- **Decision Latency ($T_{\text{dec}}$):** Time to match gesture against profile mappings and check safety constraints ($< 0.15\text{ ms}$).
- **Action Latency ($T_{\text{act}}$):** Time to invoke the backend driver ($< 0.30\text{ ms}$).
- **Total Control Overhead:** Typically $< 0.50\text{ ms}$, representing $< 2\%$ of the 60 FPS frame budget ($16.6\text{ ms}$).
- **Rotating CSV Logger:** Records events to `results/control/control_log.csv` with automatic 5MB log rotation.

---

## 6. PySide6 Engineering Dashboard Integration

Tab 10 ("10. COMPUTER CONTROL") provides real-time monitoring and interactive adjustments:
- **Top Action Bar:** Mode switch (Enable/Disable), Emergency Stop (`F12`), Reset Emergency, Profile Selector (`mouse`, `presentation`, `media`, `object3d`), and active state badge.
- **Left Panel:** Active Profile Command Mapping table showing trigger gestures, actions, target subsystems, and debounce rules.
- **Right Panel:**
  - **Control Telemetry Card:** Live status message, dispatched command, decision/action latency, and rolling P50/P95/P99 latency metrics.
  - **GA Rotor 3D Object Card:** Rotor formula, active sandwich transformation, scale factor, and vertex traces.
  - **Recent Dispatched Actions Table:** Chronological log of recent executed actions.
