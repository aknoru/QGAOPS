# Reference-model API

Import from `software.reference_model.qgaops_reference`.

```python
from software.reference_model.qgaops_reference import Multivector, blade, scalar

a = scalar(1) + blade("e1")
b = scalar(1) + blade("e2")
product = a.geometric_product(b)
assert product.coefficients == (1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0)
```

`Multivector.from_coefficients` requires exactly eight finite real values.
`blade` accepts a basis name or index. `grade_projection` accepts grades 0
through 3. Invalid shapes, non-finite coefficients, unknown blades, and
invalid grades raise clear `ValueError` or `TypeError` exceptions.

The fixed API is:

```python
from software.reference_model.qgaops_reference import FixedPointMultivector

a = FixedPointMultivector.from_reals([1.25] + [0.0] * 7)
result = a.geometric_product(a)
print(result.to_reals(), result.overflowed)
```

Fixed-point instances expose encoded integer `coefficients`, a
`FixedPointFormat`, and an `overflowed` flag. Input conversion may saturate
and reports that fact through the flag; arithmetic never silently wraps.
