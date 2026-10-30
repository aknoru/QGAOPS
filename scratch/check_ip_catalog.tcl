create_project -in_memory -part xczu5eg-sfvc784-1-e
set_property board_part tul.com.tw:pynqzu:part0:1.1 [current_project]
set_property ip_repo_paths [list D:/QGPU/HW/vitis/SEQ_GPU/work/hls/impl/ip D:/QGPU/HW/vitis/PARALLEL_GPU/work/hls/impl/ip] [current_project]
update_ip_catalog
set ips [get_ipdefs *gpu*]
puts "FOUND_IP_DEFS: $ips"
foreach ip $ips {
    puts "IP: $ip"
}
exit 0
