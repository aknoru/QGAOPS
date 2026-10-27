# Basis and metric tables

| mask | index | blade | grade |
|---:|---:|---|---:|
| 0 | 0 | 1 | 0 |
| 1 | 1 | e1 | 1 |
| 2 | 2 | e2 | 1 |
| 4 | 3 | e3 | 1 |
| 3 | 4 | e12 | 2 |
| 5 | 5 | e13 | 2 |
| 6 | 6 | e23 | 2 |
| 7 | 7 | e123 | 3 |

The metric diagonal is `(1,1,1)`. A compact hand-checkable product rule is
`(a,b) -> (a xor b, sign(a,b))`, with
`sign(a,b)=(-1)^(sum_{i>j} a_i b_j)`. Examples:

| product | result |
|---|---|
| `e1 e1` | `1` |
| `e1 e2` | `e12` |
| `e2 e1` | `-e12` |
| `e12 e3` | `e123` |
| `e3 e12` | `e123` |
| `e123 e123` | `-1` |
