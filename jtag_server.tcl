# jtag_server.tcl - Direct USB JTAG Accelerator Server
# Runs locally on your laptop, talks directly to the connected FPGA board over USB JTAG!

connect -url TCP:127.0.0.1:3121
after 500
targets -set -nocase -filter {name =~ "PSU*"}
memmap -addr 0xA0000000 -size 0x100000 -flags 3

puts "\n============================================================"
puts "  DIRECT USB JTAG FPGA ACCELERATOR SERVER READY"
puts "  Connected to Physical FPGA Board via USB JTAG!"
puts "  Listening on localhost:5005 for laptop camera input..."
puts "============================================================\n"

set ADDR_CTRL   0xA0000000
set ADDR_A_BASE 0xA0000010
set ADDR_B_BASE 0xA0000050
set ADDR_C_BASE 0xA0000090
set ADDR_OPCODE 0xA0000110

proc handle_client {sock addr port} {
    fconfigure $sock -buffering line -blocking 1
    fileevent $sock readable [list process_request $sock]
}

proc process_request {sock} {
    global ADDR_CTRL ADDR_A_BASE ADDR_B_BASE ADDR_C_BASE ADDR_OPCODE
    if {[eof $sock]} {
        close $sock
        return
    }
    set line [gets $sock]
    if {[string length [string trim $line]] == 0} {
        return
    }

    # Parse simple JSON array for a and b
    # Expected format: {"a": [0,...], "b": [0,...], "op": 1}
    set t0 [clock microseconds]
    
    # Extract operands using regex
    set a_list {}
    set b_list {}
    set op 1
    
    if {[regexp {"a"\s*:\s*\[([^\]]+)\]} $line -> a_str]} {
        set a_list [split $a_str ","]
    }
    if {[regexp {"b"\s*:\s*\[([^\]]+)\]} $line -> b_str]} {
        set b_list [split $b_str ","]
    }
    if {[regexp {"op"\s*:\s*([0-9]+)} $line -> op_val]} {
        set op $op_val
    }

    # Write Operand A (8 blades)
    for {set i 0} {$i < 8 && $i < [llength $a_list]} {incr i} {
        set val [string trim [lindex $a_list $i]]
        mwr [expr {$ADDR_A_BASE + $i * 8}] $val
    }

    # Write Operand B (8 blades)
    for {set i 0} {$i < 8 && $i < [llength $b_list]} {incr i} {
        set val [string trim [lindex $b_list $i]]
        mwr [expr {$ADDR_B_BASE + $i * 8}] $val
    }

    # Write Opcode & Start Accelerator
    mwr $ADDR_OPCODE $op
    mwr $ADDR_CTRL 1

    # Poll AP_DONE
    for {set k 0} {$k < 100} {incr k} {
        set ctrl [mrd -value $ADDR_CTRL]
        if {$ctrl & 2} {
            break
        }
    }

    # Read back Result C (8 blades)
    set c_list {}
    for {set i 0} {$i < 8} {incr i} {
        set raw [mrd -value [expr {$ADDR_C_BASE + $i * 16}]]
        if {$raw >= 2147483648} {
            set raw [expr {$raw - 4294967296}]
        }
        lappend c_list $raw
    }

    set t1 [clock microseconds]
    set lat [expr {$t1 - $t0}]

    # Format JSON response
    set resp "{\"status\": \"OK\", \"c\": \[[join $c_list ", "]\], \"pl_latency_us\": $lat}\n"
    puts -nonewline $sock $resp
    flush $sock
}

# Start TCP Server on Port 5005
socket -server handle_client 5005
vwait forever
