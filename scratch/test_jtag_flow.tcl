connect -url TCP:127.0.0.1:3121
after 500
targets -set -nocase -filter {name =~ "xczu5*" || name =~ "PL"}
puts "=== PROGRAMMING BITSTREAM OVER USB JTAG ==="
fpga -f "HW/vivado/PARALLEL_GPU_PYNQZU/export/PARALLEL_GPU_PYNQZU.bit"
puts "=== BITSTREAM PROGRAMMED! DONE LED IS ON ==="

# Select Cortex-A53 #0 to access PL AXI bus
targets -set -nocase -filter {name =~ "Cortex-A53 #0*"}
catch {memmap -addr 0xA0000000 -size 0x100000 -flags 3}

# Read Control Register at 0xA0000000
set ctrl [mrd -value 0xA0000000]
puts "Initial PL Control Register (0xA0000000): $ctrl"

# Write Operand A (e1 = 1.0 = 0x00010000 at 0xA0000018)
mwr 0xA0000018 0x00010000
# Write Operand B (e2 = 1.0 = 0x00010000 at 0xA0000060)
mwr 0xA0000060 0x00010000
# Write Opcode 1 (Geometric Product at 0xA0000110)
mwr 0xA0000110 0x00000001

# Start PL Accelerator (AP_START at 0xA0000000)
mwr 0xA0000000 0x00000001
after 10

# Read status and result C
set done_ctrl [mrd -value 0xA0000000]
set c_e12 [mrd -value 0xA00000D0] ;# blade e12 at offset 0x90 + 4*0x10 = 0xD0
puts "Post-Exec Control Register: $done_ctrl"
puts "FPGA Result Blade e12: $c_e12 (Expected 0x00010000 for e1*e2=e12)"

exit 0
