import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.0.220", username="xilinx", password="xilinx", timeout=10)
stdin, stdout, stderr = ssh.exec_command("echo xilinx | sudo -S fuser -k 5005/tcp 8080/tcp 2>/dev/null; echo xilinx | sudo -S pkill -9 -f qgpu_board.py 2>/dev/null; sleep 1; echo 'Cleaned ports 5005 and 8080'")
print(stdout.read().decode())
ssh.close()
