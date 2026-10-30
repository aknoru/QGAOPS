connect -url TCP:127.0.0.1:3121
after 500
targets -set -nocase -filter {name =~ "PSU*"}
memmap -addr 0xA0000000 -size 0x100000 -flags 3

set ctrl [mrd -value 0xA0000000]
puts "PSU Direct AXI Read (0xA0000000): $ctrl"

# Write Operand A (e1 = 1.0 = 0x00010000 at 0xA0000018)
mwr 0xA0000018 0x00010000
# Write Operand B (e2 = 1.0 = 0x00010000 at 0xA0000060)
mwr 0xA0000060 0x00010000
# Write Opcode 1 (Geometric Product at 0xA0000110)
mwr 0xA0000110 0x00000001

# Start PL Accelerator
mwr 0xA0000000 0x00000001
after 5

set done_ctrl [mrd -value 0xA0000000]
set c_e12 [mrd -value 0xA00000D0]
puts "Post-Exec Control: $done_ctrl"
puts "FPGA Direct Output (Blade e12): $c_e12 (Expected 0x00010000 / 65536)"
exit 0
