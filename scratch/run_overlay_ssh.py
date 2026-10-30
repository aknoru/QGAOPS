import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.0.220", username="xilinx", password="xilinx", timeout=10)

cmd = "/usr/local/share/pynq-venv/bin/python3 /home/xilinx/test_overlay.py"
print(f"Executing: {cmd}...")
stdin, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
err = stderr.read().decode()
print("STDOUT:\n", out)
print("STDERR:\n", err)
ssh.close()
