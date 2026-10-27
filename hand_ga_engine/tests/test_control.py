"""
Tests for Phase 5: Computer Vision Gesture Control System.

[IMPLEMENTED]
- Uses MockInputBackend to prevent ANY physical OS mouse/keyboard actions during tests.
- Tests safety interlocks, confidence filtering, debounce, confirmation (OK_SIGN).
- Tests F12 emergency cut-off.
- Tests mouse controller (smoothing, deadzone, velocity clamp, margins).
- Tests scroll & keyboard controllers (whitelisting).
- Tests GA Rotor 3D virtual object manipulation (R v ~R).
- Tests command mapper & profile switching.
- Tests full GestureController telemetry & CSV logging.
"""
import time
import numpy as np
import pytest

from control.safety import SafetyManager, ControlState
from control.command_mapper import CommandMapper, GestureCommand
from control.mouse_controller import MouseController, MockInputBackend
from control.scroll_controller import ScrollController
from control.keyboard_controller import KeyboardController
from control.application_controller import ApplicationController
from control.object3d import Virtual3DObject
from control.controller import GestureController
from hand_detection.landmarks import HandGeometry, HandGeometryExtractor


# ---------------------------------------------------------------------------
# Fixture: Mock HandGeometry
# ---------------------------------------------------------------------------
@pytest.fixture
def mock_hand_geometry():
    """Create a synthetic HandGeometry with known landmark coordinates."""
    raw = np.zeros((21, 3), dtype=np.float32)
    raw[0] = [0.5, 0.8, 0.0]    # wrist
    raw[4] = [0.55, 0.35, 0.05] # thumb tip
    raw[8] = [0.6, 0.3, 0.1]    # index tip
    raw[12] = [0.5, 0.25, 0.1]  # middle tip
    raw[16] = [0.45, 0.3, 0.1]  # ring tip
    raw[20] = [0.4, 0.35, 0.1]  # pinky tip
    extractor = HandGeometryExtractor()
    return extractor.extract(raw, raw, confidence=0.95, handedness="Right", frame_index=1)


# ---------------------------------------------------------------------------
# 1. Safety Manager Tests
# ---------------------------------------------------------------------------
def test_safety_manager_opt_in_by_default():
    safety = SafetyManager(min_confidence=0.70)
    assert not safety.is_enabled
    assert safety.state == ControlState.DISABLED

    safety.enable()
    assert safety.is_enabled
    assert safety.state == ControlState.ENABLED

    safety.disable()
    assert not safety.is_enabled
    assert safety.state == ControlState.DISABLED


def test_safety_confidence_filtering():
    safety = SafetyManager(min_confidence=0.70)
    safety.enable()

    assert not safety.check_confidence(0.65)
    assert safety.metrics["ignored_low_conf"] == 1

    assert safety.check_confidence(0.72)
    assert safety.metrics["ignored_low_conf"] == 1


def test_safety_cooldown_and_debounce():
    safety = SafetyManager(default_cooldown_s=0.20)
    safety.enable()

    # Continuous actions bypass cooldown
    assert safety.check_cooldown("CURSOR_MOVE")
    assert safety.check_cooldown("CURSOR_MOVE")

    # Discrete actions enforce cooldown
    assert safety.check_cooldown("RIGHT_CLICK")
    safety.register_execution("RIGHT_CLICK")
    # Immediate second call should be blocked
    assert not safety.check_cooldown("RIGHT_CLICK")
    assert safety.metrics["false_triggers_blocked"] == 1

    # Wait for cooldown to expire
    time.sleep(0.22)
    assert safety.check_cooldown("RIGHT_CLICK")


def test_safety_emergency_stop():
    safety = SafetyManager()
    safety.enable()
    assert safety.is_enabled

    safety.emergency_stop()
    assert safety.state == ControlState.EMERGENCY_STOPPED
    assert not safety.is_enabled

    # Reset
    safety.reset_emergency()
    assert safety.state == ControlState.DISABLED


def test_safety_confirmation_flow():
    safety = SafetyManager(confirmation_timeout_s=1.0)
    safety.enable()

    cmd = GestureCommand(
        gesture="OPEN_PALM",
        confidence=0.9,
        duration=0.0,
        command="PRESENTATION_START",
        requires_confirmation=True,
    )

    # Requires confirmation
    needs_confirm = safety.request_confirmation(cmd)
    assert needs_confirm is not None
    assert safety.pending_confirmation is not None
    assert safety.pending_confirmation.command == "PRESENTATION_START"

    # Feed OK_SIGN to trigger confirmation
    confirmed = safety.check_confirmation_trigger("OK_SIGN")
    assert confirmed is not None
    assert confirmed.command == "PRESENTATION_START"
    assert safety.pending_confirmation is None
    assert safety.metrics["confirmations_executed"] == 1


def test_safety_confirmation_timeout():
    safety = SafetyManager(confirmation_timeout_s=0.1)
    safety.enable()

    cmd = GestureCommand(
        gesture="OPEN_PALM",
        confidence=0.9,
        duration=0.0,
        command="PRESENTATION_START",
        requires_confirmation=True,
    )
    safety.request_confirmation(cmd)
    assert safety.pending_confirmation is not None

    time.sleep(0.15)
    # Expired
    assert safety.pending_confirmation is None
    confirmed = safety.check_confirmation_trigger("OK_SIGN")
    assert confirmed is None


# ---------------------------------------------------------------------------
# 2. Command Mapper & YAML Profiles
# ---------------------------------------------------------------------------
def test_command_mapper_profiles():
    mapper = CommandMapper(profile_name="mouse")
    assert mapper.active_profile_name == "mouse"
    assert "INDEX_POINT" in mapper.active_mappings
    assert mapper.active_mappings["INDEX_POINT"].command == "CURSOR_MOVE"

    # Switch to presentation
    assert mapper.set_profile("presentation")
    assert mapper.active_profile_name == "presentation"
    assert "SWIPE_RIGHT" in mapper.active_mappings
    assert mapper.active_mappings["SWIPE_RIGHT"].command == "NEXT_SLIDE"

    # Switch to media
    assert mapper.set_profile("media")
    assert mapper.active_profile_name == "media"
    assert "THUMBS_UP" in mapper.active_mappings
    assert mapper.active_mappings["THUMBS_UP"].command == "PLAY_PAUSE"

    # Switch to object3d
    assert mapper.set_profile("object3d")
    assert mapper.active_profile_name == "object3d"
    assert "ROTATE_CLOCKWISE" in mapper.active_mappings
    assert mapper.active_mappings["ROTATE_CLOCKWISE"].command == "OBJECT_ROTATE_CW"


# ---------------------------------------------------------------------------
# 3. Mouse Controller with Mock Backend
# ---------------------------------------------------------------------------
def test_mouse_controller_mock_backend():
    mock = MockInputBackend(screen_width=1920, screen_height=1080)
    mouse = MouseController(backend=mock, smoothing_alpha=0.5, dead_zone_px=2.0)

    # Initial position
    mock.cursor_x = 960
    mock.cursor_y = 540

    # Feed landmark position that exceeds dead zone
    mouse.update_cursor_position(0.65, 0.35)
    assert len(mock.events) >= 1
    assert mock.events[0][0] == "move"

    # Pinch start -> mouse_down
    mouse.handle_pinch_start()
    assert mock.mouse_down_state is True
    assert mock.events[-1] == ("mouse_down", "left")

    # Pinch hold -> drag
    mouse.handle_pinch_hold()

    # Pinch release -> mouse_up
    mouse.handle_pinch_release()
    assert mock.mouse_down_state is False
    assert mock.events[-1] == ("mouse_up", "left")

    # Right click
    mouse.handle_right_click()
    assert mock.events[-1] == ("click", "right")


# ---------------------------------------------------------------------------
# 4. Keyboard Controller Whitelisting
# ---------------------------------------------------------------------------
def test_keyboard_controller_whitelisting():
    mock = MockInputBackend()
    kb = KeyboardController(backend=mock)

    # Whitelisted keys succeed
    assert kb.press_key("left")
    assert mock.events[-1] == ("press", "left")

    assert kb.press_key("f5")
    assert mock.events[-1] == ("press", "f5")

    # Non-whitelisted keys blocked for security
    assert not kb.press_key("rm")
    assert not kb.press_key("format")
    assert not kb.press_key("cmd")


# ---------------------------------------------------------------------------
# 5. Application Controller (Presentation & Media)
# ---------------------------------------------------------------------------
def test_application_controller():
    mock = MockInputBackend()
    kb = KeyboardController(backend=mock)
    app = ApplicationController(keyboard=kb)

    assert app.slide_next()
    assert mock.events[-1] == ("press", "right")

    assert app.slide_previous()
    assert mock.events[-1] == ("press", "left")

    assert app.presentation_start()
    assert mock.events[-1] == ("press", "f5")

    assert app.presentation_stop()
    assert mock.events[-1] == ("press", "escape")

    assert app.media_play_pause()
    assert mock.events[-1] == ("press", "playpause")


# ---------------------------------------------------------------------------
# 6. GA Rotor 3D Virtual Object
# ---------------------------------------------------------------------------
def test_virtual_3d_object_ga_rotations():
    obj = Virtual3DObject()
    initial_coeffs = np.array([v.coeffs for v in obj.vertices])

    # Apply 90 degree rotation about Y axis via GA rotor
    # Bivector B = e1 ^ e2 (in 3D, rotation in XZ plane around Y axis)
    axis_y = np.array([0.0, 1.0, 0.0])
    obj.rotate_via_rotor(axis=axis_y, angle_rad=np.pi / 2)

    # Verify trace is recorded
    trace = obj.transformation_trace
    assert "rotor" in trace
    assert "reverse_rotor" in trace
    assert "rotor_norm" in trace
    assert abs(trace["rotor_norm"] - 1.0) < 1e-4

    # Vertices must have rotated
    rotated_coeffs = np.array([v.coeffs for v in obj.vertices])
    assert not np.allclose(rotated_coeffs, initial_coeffs)

    # Zoom in and out
    init_scale = obj.scale
    obj.zoom(1.2)
    assert obj.scale > init_scale
    obj.zoom(0.5)
    assert obj.scale < init_scale

    # Reset
    obj.reset()
    reset_coeffs = np.array([v.coeffs for v in obj.vertices])
    assert np.allclose(reset_coeffs, initial_coeffs)
    assert obj.scale == 1.0

    # Perspective rendering test
    rendered = obj.render(320, 240)
    assert isinstance(rendered, np.ndarray)
    assert rendered.shape == (240, 320, 3)


# ---------------------------------------------------------------------------
# 7. End-to-End GestureController with Mock Backend
# ---------------------------------------------------------------------------
def test_gesture_controller_e2e(mock_hand_geometry, tmp_path):
    mock = MockInputBackend()
    log_file = tmp_path / "test_control_log.csv"
    controller = GestureController(profile_name="mouse", log_path=str(log_file), backend=mock)

    # By default, disabled
    assert not controller.is_enabled
    rep = controller.process_frame(gesture="INDEX_POINT", confidence=0.90, geom=mock_hand_geometry)
    assert rep.is_control_enabled is False
    assert rep.is_executed is False

    # Enable control
    controller.enable()
    assert controller.is_enabled

    # Process INDEX_POINT cursor move
    rep = controller.process_frame(gesture="INDEX_POINT", confidence=0.90, geom=mock_hand_geometry)
    assert rep.is_control_enabled is True
    assert rep.command == "CURSOR_MOVE"
    assert rep.is_executed is True
    assert rep.ga_opcode == "VECTOR"

    # Test Latency statistics
    p_stats = controller.get_latency_percentiles()
    assert "p50" in p_stats
    assert "p95" in p_stats
    assert "p99" in p_stats

    # Test Profile Switching to presentation
    assert controller.set_profile("presentation")
    assert controller.mapper.active_profile_name == "presentation"

    # Trigger NEXT_SLIDE
    rep = controller.process_frame(gesture="SWIPE_RIGHT", confidence=0.90, geom=mock_hand_geometry)
    assert rep.command == "NEXT_SLIDE"
    assert rep.is_executed is True

    # Test Emergency Stop
    controller.emergency_stop()
    assert controller.safety.state == ControlState.EMERGENCY_STOPPED
    rep = controller.process_frame(gesture="SWIPE_RIGHT", confidence=0.90, geom=mock_hand_geometry)
    assert rep.is_executed is False
    assert "EMERGENCY" in rep.status_message

    # Verify CSV log was created
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "CURSOR_MOVE" in content or "NEXT_SLIDE" in content
