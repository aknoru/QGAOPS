# Stage 4 test report

## Status

Stage 4 is complete after the test command below passes. The report records
the current implementation and does not claim any hardware behavior.

## Command and evidence

```powershell
.\.venv\Scripts\python.exe -m pytest software\reference_model\tests -q
```

Executed result: `9 passed in 0.23s` under Python 3.13.14 with pytest 8.4.2.

The suite contains:

- 64 floating-point geometric-product basis pairs.
- 64 floating-point wedge basis pairs.
- 64 floating-point Hestenes-inner basis pairs.
- 64 fixed-point geometric-product basis pairs.
- 64 fixed-point wedge basis pairs.
- 64 fixed-point Hestenes-inner basis pairs.
- Basis identities, bilinearity, associativity, involutions, grade
  reconstruction, validation errors, conversion rounding, endpoint
  saturation, intermediate arithmetic, and differential checks.

The exact pass/fail summary is updated only after the command is executed in
the current environment. The model uses no NumPy dependency and no hardware
implementation.
