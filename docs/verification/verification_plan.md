# Verification and acceptance plan

Offline checks now include reference-model tests, seeded benchmark and fixture
tests, dashboard backend smoke tests, interface serialization tests, structure,
Markdown, citation-key, CSV, YAML, and Mermaid-source checks. Stage 10 will
add HLS C-simulation/cosimulation, synthesis resource reports,
timing, protocol tests, and physical PS/PL transactions.

Benchmark reports must separate CPU baseline, kernel-only, transfer-only, and
end-to-end timings; disclose clock, batch size, precision, workload
distribution, tool versions, and whether warm-up is included. Resource and
power values must identify their measurement source and boundary.
