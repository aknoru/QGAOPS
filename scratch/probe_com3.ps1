$port = New-Object System.IO.Ports.SerialPort('COM3', 115200)
$port.ReadTimeout = 2000
try {
    $port.Open()
    $port.WriteLine("ps -ef | grep server")
    Start-Sleep -Milliseconds 600
    $out = ""
    while ($port.BytesToRead -gt 0) {
        $out += [char]$port.ReadChar()
    }
    $port.Close()
    Write-Host "COM3_OUTPUT: $out"
} catch {
    Write-Host "ERROR: $($_.Exception.Message)"
}
