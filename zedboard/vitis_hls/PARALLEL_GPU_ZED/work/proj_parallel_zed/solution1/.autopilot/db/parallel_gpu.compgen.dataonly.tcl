# This script segment is generated automatically by AutoPilot

set axilite_register_dict [dict create]
set port_control {
a_0 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 16
	offset_end 23
}
a_1 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 24
	offset_end 31
}
a_2 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 32
	offset_end 39
}
a_3 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 40
	offset_end 47
}
a_4 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 48
	offset_end 55
}
a_5 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 56
	offset_end 63
}
a_6 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 64
	offset_end 71
}
a_7 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 72
	offset_end 79
}
b_0 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 80
	offset_end 87
}
b_1 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 88
	offset_end 95
}
b_2 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 96
	offset_end 103
}
b_3 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 104
	offset_end 111
}
b_4 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 112
	offset_end 119
}
b_5 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 120
	offset_end 127
}
b_6 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 128
	offset_end 135
}
b_7 { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 136
	offset_end 143
}
c_0 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 144
	offset_end 151
}
c_1 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 160
	offset_end 167
}
c_2 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 176
	offset_end 183
}
c_3 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 192
	offset_end 199
}
c_4 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 208
	offset_end 215
}
c_5 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 224
	offset_end 231
}
c_6 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 240
	offset_end 247
}
c_7 { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 256
	offset_end 263
}
opcode { 
	dir I
	width 32
	depth 1
	mode ap_none
	offset 272
	offset_end 279
}
status { 
	dir O
	width 32
	depth 1
	mode ap_vld
	offset 280
	offset_end 287
}
ap_start { }
ap_done { }
ap_ready { }
ap_idle { }
interrupt {
}
}
dict set axilite_register_dict control $port_control


