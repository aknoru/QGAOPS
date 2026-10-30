## ==============================================================================
## QGAOPS-QGPU: Project Constraints File for AMD PYNQ-ZU Rev B
## Target FPGA Part: xczu5eg-sfvc784-1-e
## Accelerator: PARALLEL_GPU only (STAGE 14 frozen)
##
## Electrical Rules:
##   Bank 66 VCCO = 1.2V  -> PL User LEDs, RGB LEDs use LVCMOS12
##   Bank 44 VCCO = 1.2V  -> Push Buttons and DIP Switches use LVCMOS12
##   Bank 65 VCCO = 1.8V  -> User Reset (URST_B) uses LVCMOS18
##
## LED Signal Semantics (wired to qgpu_led_controller outputs):
##   LED0 (B5) = IDLE / READY     -- solid ON when accelerator is idle
##   LED1 (A6) = AP_START / BUSY  -- 40 ms stretched pulse on each operation start
##   LED2 (B8) = AP_DONE / RESULT -- 40 ms stretched pulse on each completion
##   LED3 (A7) = ERROR / OVERFLOW -- sticky ON when overflow or invalid opcode fired
##
## References:
##   PYNQ-ZU Reference User Manual v1.2, Sections 12-15
##   XUP-ZU5EG Schematic Rev 3.B (XUP-ZU5EG-20200824.pdf)
## ==============================================================================

# ------------------------------------------------------------------------------
# 1. PL User LEDs -- qgpu_led_controller outputs
#    Bank 66, VCCO = 1.2V, LVCMOS12
#    Mapped to wrapper port: led_o[3:0]
# ------------------------------------------------------------------------------
set_property PACKAGE_PIN B5 [get_ports {led_o[0]}];  # LED0 = IDLE/READY
set_property PACKAGE_PIN A6 [get_ports {led_o[1]}];  # LED1 = BUSY/AP_START
set_property PACKAGE_PIN B8 [get_ports {led_o[2]}];  # LED2 = DONE/AP_DONE
set_property PACKAGE_PIN A7 [get_ports {led_o[3]}];  # LED3 = ERROR/OVERFLOW

set_property IOSTANDARD LVCMOS12 [get_ports {led_o[*]}]
set_property DRIVE        8       [get_ports {led_o[*]}]
set_property SLEW         SLOW    [get_ports {led_o[*]}]

# Timing exception: LEDs are asynchronous outputs, no timing path required
set_false_path -to [get_ports {led_o[*]}]

# ------------------------------------------------------------------------------
# 2. PL RGB LEDs (Bank 66, VCCO = 1.2V) -- Unused in this build, constrained
#    to prevent DRC errors if top-level wrapper exposes them
# ------------------------------------------------------------------------------
# RGB0
set_property PACKAGE_PIN A9 [get_ports {rgb_led0[0]}];  # LED_B0 (Blue)
set_property PACKAGE_PIN A5 [get_ports {rgb_led0[1]}];  # LED_G0 (Green)
set_property PACKAGE_PIN A4 [get_ports {rgb_led0[2]}];  # LED_R0 (Red)
set_property IOSTANDARD LVCMOS12 [get_ports {rgb_led0[*]}]
set_property DRIVE        8       [get_ports {rgb_led0[*]}]
set_property SLEW         SLOW    [get_ports {rgb_led0[*]}]

# RGB1
set_property PACKAGE_PIN A8 [get_ports {rgb_led1[0]}];  # LED_B1 (Blue)
set_property PACKAGE_PIN B9 [get_ports {rgb_led1[1]}];  # LED_G1 (Green)
set_property PACKAGE_PIN B6 [get_ports {rgb_led1[2]}];  # LED_R1 (Red)
set_property IOSTANDARD LVCMOS12 [get_ports {rgb_led1[*]}]
set_property DRIVE        8       [get_ports {rgb_led1[*]}]
set_property SLEW         SLOW    [get_ports {rgb_led1[*]}]

set_false_path -to [get_ports {rgb_led0[*]}]
set_false_path -to [get_ports {rgb_led1[*]}]

# ------------------------------------------------------------------------------
# 3. User Push Buttons (Bank 44, VCCO = 1.2V, Active High)
# ------------------------------------------------------------------------------
set_property PACKAGE_PIN AH14 [get_ports {pl_btns[0]}]
set_property PACKAGE_PIN AG14 [get_ports {pl_btns[1]}]
set_property PACKAGE_PIN AE14 [get_ports {pl_btns[2]}]
set_property PACKAGE_PIN AE15 [get_ports {pl_btns[3]}]
set_property IOSTANDARD LVCMOS12 [get_ports {pl_btns[*]}]
set_false_path -from [get_ports {pl_btns[*]}]

# ------------------------------------------------------------------------------
# 4. User DIP Switches (Bank 44, VCCO = 1.2V)
# ------------------------------------------------------------------------------
set_property PACKAGE_PIN AA12 [get_ports {pl_sws[0]}]
set_property PACKAGE_PIN Y12  [get_ports {pl_sws[1]}]
set_property PACKAGE_PIN W11  [get_ports {pl_sws[2]}]
set_property PACKAGE_PIN W12  [get_ports {pl_sws[3]}]
set_property IOSTANDARD LVCMOS12 [get_ports {pl_sws[*]}]
set_false_path -from [get_ports {pl_sws[*]}]

# ------------------------------------------------------------------------------
# 5. User Reset Push Button (Active Low, Bank 65, VCCO = 1.8V)
# ------------------------------------------------------------------------------
set_property PACKAGE_PIN H2 [get_ports {user_rst_n}]
set_property IOSTANDARD LVCMOS18 [get_ports {user_rst_n}]
set_false_path -from [get_ports {user_rst_n}]

# ------------------------------------------------------------------------------
# 6. Clocks -- PS pl_clk0 is auto-constrained by Zynq UltraScale+ IP
#    External differential reference clocks constrained for completeness
# ------------------------------------------------------------------------------
# 125 MHz diff ref (Si5340 Ch2) -- used only if needed by designs
set_property PACKAGE_PIN K4 [get_ports {sys_clk_125_p}]
set_property PACKAGE_PIN K3 [get_ports {sys_clk_125_n}]
set_property IOSTANDARD LVDS [get_ports {sys_clk_125_p}]
set_property IOSTANDARD LVDS [get_ports {sys_clk_125_n}]
create_clock -period 8.000 -name sys_clk_125 [get_ports sys_clk_125_p]
