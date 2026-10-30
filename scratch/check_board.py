import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.0.220", username="xilinx", password="xilinx", timeout=10)
stdin, stdout, stderr = ssh.exec_command("ps aux | grep qgpu; ls -la /home/xilinx/pynq_board_package/web; ls -la /home/xilinx/web 2>/dev/null")
print(stdout.read().decode())
ssh.close()
