"""
LIVE HAND GA ENGINE — metrics/hardware_metrics.py
Hardware counter interface for future FPGA / Zynq PL accelerator.

[PROPOSED] Interface specification for ZedBoard / Zynq-7000 FPGA execution.
[NOT IMPLEMENTED] No FPGA hardware connected. Returns NOT_AVAILABLE.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


NOT_AVAILABLE = "N/A — FPGA not connected"
NOT_SYNTHESIZED = "N/A — FPGA not synthesized"


@dataclass
class HardwareMetrics:
    """Hardware counter report.

    [PROPOSED] Every field clearly indicates hardware availability status.
    NEVER fake hardware metrics.
    """
    fpga_connected:        bool = False
    target_device:         str  = "Xilinx Zynq-7000 (XC7Z020-CLG484-1)"
    lut:                   str  = NOT_SYNTHESIZED
    ff:                    str  = NOT_SYNTHESIZED
    bram:                  str  = NOT_SYNTHESIZED
    dsp:                   str  = NOT_SYNTHESIZED
    fmax_mhz:              str  = NOT_SYNTHESIZED
    cycles:                str  = NOT_AVAILABLE
    hardware_latency_us:   str  = NOT_AVAILABLE
    hardware_throughput:   str  = NOT_AVAILABLE
    axi_read_bytes:        str  = NOT_AVAILABLE
    axi_write_bytes:       str  = NOT_AVAILABLE
    ddr_bandwidth_mbs:     str  = NOT_AVAILABLE
    power_w:               str  = NOT_AVAILABLE
    energy_per_op_uj:      str  = NOT_AVAILABLE
    status:                str  = NOT_AVAILABLE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fpga_connected": self.fpga_connected,
            "target_device": self.target_device,
            "lut": self.lut,
            "ff": self.ff,
            "bram": self.bram,
            "dsp": self.dsp,
            "fmax_mhz": self.fmax_mhz,
            "cycles": self.cycles,
            "hardware_latency_us": self.hardware_latency_us,
            "hardware_throughput": self.hardware_throughput,
            "axi_read_bytes": self.axi_read_bytes,
            "axi_write_bytes": self.axi_write_bytes,
            "ddr_bandwidth_mbs": self.ddr_bandwidth_mbs,
            "power_w": self.power_w,
            "energy_per_op_uj": self.energy_per_op_uj,
            "status": self.status,
            "classification": "[N/A — FPGA NOT CONNECTED]",
        }


class HardwareMetricsInterface:
    """Interface for physical accelerator counters.

    [PROPOSED] Future Zynq Linux driver/mmap will read AXI Lite performance registers.
    """

    def __init__(self, device_path: Optional[str] = None) -> None:
        self.device_path = device_path
        self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected

    def read_counters(self) -> HardwareMetrics:
        """Query physical accelerator counters.

        Returns HardwareMetrics with explicit 'N/A — FPGA not connected' values.
        """
        return HardwareMetrics(
            fpga_connected=False,
            status=NOT_AVAILABLE,
        )
