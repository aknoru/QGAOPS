#!/usr/bin/env bash
# ==============================================================================
# run.sh - PYNQ-ZU Convenience Runner for QGAOPS-QGPU
# ==============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="/usr/local/share/pynq-venv/bin/python3"

if [ ! -f "$PYTHON" ]; then
    PYTHON="$(which python3)"
fi

# Detect package dir if run from /home/xilinx
if [ -f "$SCRIPT_DIR/pynq_board_package/qgpu_board.py" ]; then
    TARGET_DIR="$SCRIPT_DIR/pynq_board_package"
elif [ -f "$SCRIPT_DIR/qgpu_board.py" ]; then
    TARGET_DIR="$SCRIPT_DIR"
else
    TARGET_DIR="/home/xilinx/pynq_board_package"
fi

cd "$TARGET_DIR"

echo "=========================================================="
echo "  Starting QGPU Master Application"
echo "  Python: $PYTHON"
echo "  Directory: $TARGET_DIR"
echo "=========================================================="

# Automatically free any previous instances holding port 5005 or 8080
sudo fuser -k 5005/tcp 8080/tcp 2>/dev/null || true

sudo "$PYTHON" "$TARGET_DIR/qgpu_board.py" "$@"

