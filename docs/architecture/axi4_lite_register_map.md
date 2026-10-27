# Proposed AXI4-Lite register map

Offsets are proposals only; no AXI functionality is implemented or tested.
All registers are 32-bit, naturally aligned, and little-endian.

| Offset | Name | Access | Reset | Meaning |
|---:|---|---|---:|---|
| 0x00 | CONTROL | RW | 0 | bit 0 start, bit 1 soft reset |
| 0x04 | STATUS | RO | 0 | bit 0 busy, bit 1 done, bit 2 error |
| 0x08 | OPERATION | RW | 0 | operation identifier |
| 0x0C | BATCH_LENGTH | RW | 0 | validated batch count |
| 0x10 | VERSION | RO | 1 | interface version |
| 0x14 | ERROR_CODE | RO | 0 | proposed error code |
| 0x18 | CAPABILITIES | RO | 0 | supported-operation bitmap |
| 0x1C | CONTROL_FLAGS | RW | 0 | interrupt enable and reserved bits |

Address registers are intentionally omitted until the bulk-transfer choice is
reviewed. Writes while busy are rejected by contract. Start is a one-write
request; done is cleared by reset or a new accepted request. Reserved bits
must be written zero and read zero.
