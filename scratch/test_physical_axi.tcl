connect -url TCP:127.0.0.1:3121
after 500
targets -set -nocase -filter {name =~ "Cortex-A53 #0*"}
catch {memmap -addr 0xA0000000 -size 0x100000 -flags 3}

# Read physical address
set ctrl [mrd -physical -value 0xA0000000]
puts "Physical AXI Read: Control Register = $ctrl"

# Write Operand A (e1 = 1.0 = 0x00010000)
mwr -physical 0xA0000018 0x00010000
# Write Operand B (e2 = 1.0 = 0x00010000)
mwr -physical 0xA0000060 0x00010000
# Write Opcode 1 (Geometric Product)
mwr -physical 0xA0000110 0x00000001

# Start PL Accelerator
mwr -physical 0xA0000000 0x00000001
after 5

set done_ctrl [mrd -physical -value 0xA0000000]
set c_e12 [mrd -physical -value 0xA00000D0]
puts "Post-Exec Control: $done_ctrl"
puts "FPGA Physical Output (Blade e12): $c_e12"

exit 0
