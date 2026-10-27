# Related-work comparison

`NR` means the supplied source did not report the dimension in a form audited
here; it is not an estimate.

| Work | Algebra/workload | Architecture | Device/integration | Sharing/pipeline | Metrics boundary | Relevance |
|---|---|---|---|---|---|---|
| Huthmann 2008 | GA expressions | compiled reconfigurable accelerator | FPGA, exact target differs | configurable, NR | reported paper metrics | compiler/configuration prior art |
| Franchini 2009 | GA graphics | embedded FPGA coprocessor | FPGA, embedded system | native GA datapath, NR | application evaluation | embedded integration precedent |
| Lange 2009 | GA inverse kinematics | reconfigurable computer and GPU | platform-specific | parallel acceleration | comparative execution/energy | warns about boundary comparability |
| Hildenbrand 2017 | arbitrary GAPP GA programs | configurable GAPPCO | FPGA context, exact target differs | configurable program mapping | paper metrics | programmable GA coprocessor |
| Mishra 2015 | color edge detection | dedicated GA coprocessor | ASIC/FPGA-oriented design | application datapath | application metrics | workload-specific co-processor |
| Hara-Azumi 2013 | HLS benchmarks | shared/unshared resources | multiple FPGA devices | explicit sharing study | area/frequency/time | sharing methodology |
| Bai 2023 | HLS benchmark suite | HLS design-space evaluation | FPGA-targeted | pragma variants | benchmark/resource metrics | reproducible HLS evaluation |
| QGAOPS-QGPU | Cl(3,0), planned mixed workloads | sequential and adaptive variants | PYNQ-Z2 | AAMF hypothesis | CPU/kernel/transfer/E2E | proposed controlled comparison |

Exact LUT/FF/BRAM/DSP counts, clocks, and speedups are `NR` here unless
reported in a future audited extraction. They must not be copied across
platforms.
