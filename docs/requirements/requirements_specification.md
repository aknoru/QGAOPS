# Requirements specification

## Scope and evidence

This specification derives requirements from the attached master execution
prompt (`Pasted text #1.txt`) and the supplied research PDFs. The three named
project requirement documents are not present in the workspace; their absence
is tracked in the unresolved-decisions register. Requirements below are
therefore baseline requirements, not a claim that those missing documents were
reviewed.

## Objectives and questions

QGAOPS-QGPU will investigate whether an algebra-aware memory organization and
configurable fixed-point datapath can provide a measurable area/latency/energy
trade-off for Cl(3,0) workloads on a PYNQ-Z2. The research questions are listed
in the master prompt and are operationalized by the comparison and verification
plans.

## Functional requirements

| ID | Requirement | Acceptance evidence |
|---|---|---|
| FR-01 | Use Cl(3,0), basis order `1,e1,e2,e3,e12,e13,e23,e123`. | Mathematical specification and tests |
| FR-02 | Define geometric, outer, Hestenes inner, additive, scalar, grade, reverse, involution, and conjugation operations. | `docs/mathematics/` |
| FR-03 | Define a signed 32-bit Q16.16 initial evaluation format. | Fixed-point specification |
| FR-04 | Keep an independent software reference separate from hardware. | Future-stage interface plan |
| FR-05 | Compare sequential resource-shared and adaptive-pipeline variants under one contract. | Architecture and verification plans |
| FR-06 | Provide control, data movement, status, and error interfaces for future PL integration. | System and transaction diagrams |
| FR-07 | Record published measurements separately from proposed measurements. | Research audit and benchmark plan |

## Non-functional requirements

- Reproducible offline documentation validation must not require FPGA tools.
- Every research claim must map to a citation or be labeled engineering
  inference/proposal.
- Missing, restricted, or unreported evidence must be recorded as `NR`, not
  estimated.
- Future implementation status must be labeled planned until verified.
- The architecture must preserve a fair CPU, kernel, transfer, and
  end-to-end measurement boundary.

## Constraints and assumptions

The target is the PYNQ-Z2 reference board and its XC7Z020 Zynq device
[PYNQ2018]. The initial algebra is Euclidean and non-degenerate. The first
fixed-point candidate is Q16.16, but range suitability remains an empirical
decision. AAMF is a proposed organization, not a demonstrated optimization.

## Explicit exclusions

Stages 1–3 do not implement a reference model, HLS kernel, Vivado design,
PYNQ overlay, camera pipeline, dashboard, or benchmark results. “Quantum” in
the project name does not imply quantum hardware.
