import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.0.220", username="xilinx", password="xilinx", timeout=10)

stdin, stdout, stderr = ssh.exec_command("cat /home/xilinx/test_overlay_nohwh.py; echo '---'; cat /home/xilinx/test_mmio.py")
print(stdout.read().decode())
ssh.close()
