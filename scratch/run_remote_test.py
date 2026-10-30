import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.0.220", username="xilinx", password="xilinx", timeout=10)

cmd = "echo xilinx | sudo -S /usr/local/share/pynq-venv/bin/python3 /home/xilinx/pynq_board_package/qgpu_board.py --mode validate"
print(f"Executing: {cmd}...")
stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
for line in iter(stdout.readline, ""):
    print(line, end="")

ssh.close()
