connect -url TCP:127.0.0.1:3121
after 500
targets -set -nocase -filter {name =~ "Cortex-A53 #0*"}

# Read Physical Address space (PA)
set ctrl [mrd -address-space PA -value 0xA0000000]
puts "PA AXI Read: Control Register = $ctrl"

# Write Operand A (e1 = 1.0 = 0x00010000 at 0xA0000018)
mwr -address-space PA 0xA0000018 0x00010000
# Write Operand B (e2 = 1.0 = 0x00010000 at 0xA0000060)
mwr -address-space PA 0xA0000060 0x00010000
# Write Opcode 1 (Geometric Product at 0xA0000110)
mwr -address-space PA 0xA0000110 0x00000001

# Start PL Accelerator (0xA0000000 = 0x01)
mwr -address-space PA 0xA0000000 0x00000001
after 5

set done_ctrl [mrd -address-space PA -value 0xA0000000]
set c_e12 [mrd -address-space PA -value 0xA00000D0]
puts "Post-Exec Control: $done_ctrl"
puts "FPGA Output (Blade e12): $c_e12 (Expected 0x00010000 / 65536)"

exit 0
