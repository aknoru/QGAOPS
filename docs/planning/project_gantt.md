# Project timeline

```mermaid
gantt
  title QGAOPS-QGPU illustrative plan
  dateFormat  YYYY-MM-DD
  axisFormat  %b
  section Stage 1
  Requirements and source audit :s1a, 2026-01-05, 10d
  Literature and comparison     :s1b, after s1a, 15d
  Research-gap analysis         :s1c, after s1b, 5d
  Stage 1 gate                  :milestone, s1g, after s1c, 0d
  section Stage 2
  Basis and product conventions :s2a, after s1g, 10d
  Fixed-point semantics         :s2b, after s2a, 7d
  Examples and acceptance tests :s2c, after s2b, 7d
  Stage 2 gate                  :milestone, s2g, after s2c, 0d
  section Stage 3
  Repository and tooling        :s3a, after s2g, 7d
  Documentation and diagrams    :s3b, after s3a, 10d
  Validation and audit          :s3c, after s3b, 5d
  Stage 3 gate                  :milestone, s3g, after s3c, 0d
  section Stages 4-9
  Reference model               :s4, after s3g, 10d
  Validation and CPU baselines  :s5, after s4, 10d
  Gesture pipeline and fixture  :s6, after s5, 10d
  Dashboard and data schemas    :s7, after s6, 10d
  Hardware contract architecture:s8, after s7, 10d
  Stages 4-9 gate               :milestone, s9g, after s8, 0d
  section Planned
  Baseline HLS accelerator      :p1, after s9g, 20d
  HLS variants and Vivado       :p2, after p1, 35d
  Board and benchmark campaign  :p3, after p2, 25d
  Application integration       :p4, after p3, 20d
  Final report                  :p5, after p4, 10d
```

Dates are illustrative planning dates, not claims of completed work. The
critical path is the mathematical contract -> reference -> HLS -> board
validation sequence; failures return to the preceding gate.
