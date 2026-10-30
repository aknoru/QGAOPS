connect -url TCP:127.0.0.1:3121
after 500
targets -set -nocase -filter {name =~ "Cortex-A53 #0*"}

# Read via ARM DAP (Direct Access Port)
set ctrl [mrd -arm-dap -value 0xA0000000]
puts "DAP AXI Read: Control Register = $ctrl"

# Write Operand A (e1 = 1.0 = 0x00010000 at 0xA0000018)
mwr -arm-dap 0xA0000018 0x00010000
# Write Operand B (e2 = 1.0 = 0x00010000 at 0xA0000060)
mwr -arm-dap 0xA0000060 0x00010000
# Write Opcode 1 (Geometric Product at 0xA0000110)
mwr -arm-dap 0xA0000110 0x00000001

# Start PL Accelerator (0xA0000000 = 0x01)
mwr -arm-dap 0xA0000000 0x00000001
after 5

set done_ctrl [mrd -arm-dap -value 0xA0000000]
set c_e12 [mrd -arm-dap -value 0xA00000D0]
puts "Post-Exec Control: $done_ctrl"
puts "FPGA Output (Blade e12): $c_e12 (Expected 0x00010000 / 65536)"

exit 0
