import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.0.220", username="xilinx", password="xilinx", timeout=10)

stdin, stdout, stderr = ssh.exec_command("sed -n '40,75p' /home/xilinx/pynq/pl_server/device.py")
print(stdout.read().decode())
ssh.close()
