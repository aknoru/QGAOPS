# Literature review

## Evidence reviewed

The workspace contains papers on compiling GA to reconfigurable hardware
[Huthmann2008], GA coprocessors [Franchini2009; Hildenbrand2017],
GA acceleration on reconfigurable computers and GPUs [Lange2009], HLS resource
sharing [HaraAzumi2013], HLS benchmarking [Bai2023], and the PYNQ-Z2 board
[PYNQ2018]. The supplied `electronics-04-00094.pdf` is an open-access GA
co-processor paper [Mishra2015]. All nine files are listed in the manifest;
the duplicate DagSemProc filenames have identical size and extracted content.

## Findings

Huthmann et al. compile GA expressions into configurable hardware, making
compile-time mapping a central alternative to a fixed operation datapath.
Franchini et al. describe an embedded FPGA coprocessor with native GA support,
while GAPPCO uses configurable GAPP programs [Hildenbrand2017]. Lange et al.
compare reconfigurable computers and GPUs for inverse kinematics, illustrating
that measurement boundary and platform matter [Lange2009]. Mishra et al.
demonstrate a dedicated GA co-processor for color edge detection, but its
application and device context are not directly comparable [Mishra2015].

Hara-Azumi et al. show empirically that sharing can affect area, frequency,
and execution time in non-obvious ways [HaraAzumi2013]; therefore “no
pipeline directive” is not evidence of one physical unit. Bai et al. provide
an HLS benchmark dataset and emphasize the large design space created by
directives [Bai2023]. The PYNQ-Z2 manual establishes the board-level PS/PL
context but does not validate this project’s kernel [PYNQ2018].

## Research interpretation

The supplied evidence supports investigating configurable GA datapaths,
resource sharing, and measurement discipline. It does not establish that
AAMF improves performance, that Q16.16 is sufficient, or that a PYNQ-Z2
implementation will outperform a CPU. Those are hypotheses for later stages.
