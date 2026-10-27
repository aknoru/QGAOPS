# Stage 5 validation report

Stage 4 was rerun before this milestone: `9 passed` in the reference-model
suite. The expanded tests cover deterministic workloads, the software-only
gesture fixture, and hardware-contract round trips in addition to the
exhaustive basis-pair and fixed-point tests.

The accumulator analysis proposes a signed 66-bit raw sum for the current
Q16.16 Cl(3,0) contract because each output blade has at most eight
contributing pairs. This is a future hardware proposal, not a synthesis or
implementation result.
