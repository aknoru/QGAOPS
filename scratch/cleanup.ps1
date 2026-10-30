Remove-Item -Recurse -Force 'd:\QGPU\hardware' -ErrorAction SilentlyContinue
Write-Host "Deleted: d:\QGPU\hardware (1 GB legacy folder)"

Get-ChildItem 'd:\QGPU\HW\vivado\PARALLEL_GPU_PYNQZU' -Filter '*.jou' | Remove-Item -Force
Get-ChildItem 'd:\QGPU\HW\vivado\PARALLEL_GPU_PYNQZU' -Filter '*.backup.jou' | Remove-Item -Force
Get-ChildItem 'd:\QGPU\HW\vivado\PARALLEL_GPU_PYNQZU' -Filter '*.backup.log' | Remove-Item -Force
Write-Host "Deleted: Vivado journals and backup logs"

Remove-Item -Force 'd:\QGPU\xvlog.pb' -ErrorAction SilentlyContinue
Write-Host "Deleted: xvlog.pb"

$files = @(
  'd:\QGPU\blink_led.py',
  'd:\QGPU\check_gpio_remote.py',
  'd:\QGPU\inspect_remote.py',
  'd:\QGPU\deploy_updated_server.py',
  'd:\QGPU\remote_exec.py',
  'd:\QGPU\serial_cmd.py',
  'd:\QGPU\transfer_to_board.py',
  'd:\QGPU\transfer_robust.py',
  'd:\QGPU\connect_wifi.py',
  'd:\QGPU\check_uart.ps1',
  'd:\QGPU\probe_board.ps1',
  'd:\QGPU\probe_jtag.tcl',
  'd:\QGPU\probe_xsdb.tcl',
  'd:\QGPU\help_memmap.tcl',
  'd:\QGPU\test_seq_board.tcl',
  'd:\QGPU\test_seq_op.tcl',
  'd:\QGPU\dfx_runtime.txt',
  'd:\QGPU\pynq_app.py',
  'd:\QGPU\run_stage15_hardware.py',
  'd:\QGPU\board_benchmark.py',
  'd:\QGPU\board_server.py'
)
foreach ($p in $files) {
  Remove-Item -Force $p -ErrorAction SilentlyContinue
  Write-Host "Deleted: $p"
}

Get-ChildItem 'd:\QGPU' -Filter 'bench_*.tcl' | Remove-Item -Force
Get-ChildItem 'd:\QGPU' -Filter 'bench_*.json' | Remove-Item -Force
Get-ChildItem 'd:\QGPU' -Filter 'run_par_board.tcl' | Remove-Item -Force
Get-ChildItem 'd:\QGPU' -Filter 'run_seq_board.tcl' | Remove-Item -Force
Write-Host "Deleted: root bench_*.tcl, bench_*.json, run_*_board.tcl"

Write-Host "`nCleanup complete."
