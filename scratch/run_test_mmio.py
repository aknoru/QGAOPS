import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.0.220", username="xilinx", password="xilinx", timeout=10)

stdin, stdout, stderr = ssh.exec_command("echo xilinx | sudo -S /usr/local/share/pynq-venv/bin/python3 /home/xilinx/test_mmio.py")
print("STDOUT:\n", stdout.read().decode())
print("STDERR:\n", stderr.read().decode())
ssh.close()
