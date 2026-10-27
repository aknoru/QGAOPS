# Independent software reference model

This Stage 4 model is the mathematical oracle for future HLS and FPGA work.
It contains independent floating-point and integer-arithmetic fixed-point
paths and does not import hardware code.

## Run

From the repository root:

```powershell
.\.venv\Scripts\python.exe -m pytest software\reference_model\tests -q
.\.venv\Scripts\python.exe -m software.reference_model
```

The package uses only the Python standard library. The fixed-point format is
signed Q16.16. Products use signed integer products and an arbitrary-precision
Python accumulator before round-to-nearest-even rescaling; this avoids silent
loss while the future hardware accumulator width is characterized.
