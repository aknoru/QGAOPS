# ==============================================================================
# Makefile for QGAOPS-QGPU Vitis HLS GA Engine
# ==============================================================================

CXX = g++
CXXFLAGS = -O3 -Wall -Wextra -I../include

SRCS = ../tb/tb_qgpu_ga_engine.cpp \
       ../src/qgpu_ga_top.cpp \
       ../src/qgpu_ga_engine_shared.cpp \
       ../src/qgpu_ga_engine_parallel.cpp

BIN = ../tb/tb_qgpu_ga_engine.exe

all: test_host

test_host: $(BIN)
	$(BIN) ../vectors/golden_vectors.csv

$(BIN): $(SRCS)
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(BIN)

# Vitis HLS Toolchain Targets (requires vitis_hls on PATH)
csim:
	vitis_hls -f run_hls_csim.tcl

synth:
	vitis_hls -f run_hls_synthesis.tcl

cosim:
	vitis_hls -f run_hls_cosim.tcl

ip:
	vitis_hls -f export_hls_ip.tcl

clean:
	rm -f $(BIN)
	rm -rf prj_*
