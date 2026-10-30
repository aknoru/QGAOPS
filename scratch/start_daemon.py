import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.0.220", username="xilinx", password="xilinx", timeout=10)

# Kill old instances and start fresh daemon
cmd = "echo xilinx | sudo -S bash -c 'pkill -9 -f qgpu_board.py; fuser -k 5005/tcp 8080/tcp 2>/dev/null; sleep 1; nohup /usr/local/share/pynq-venv/bin/python3 /home/xilinx/pynq_board_package/qgpu_board.py --mode gui > /home/xilinx/qgpu_gui.log 2>&1 &'"
stdin, stdout, stderr = ssh.exec_command(cmd)
time.sleep(3)

stdin, stdout, stderr = ssh.exec_command("ps aux | grep qgpu; cat /home/xilinx/qgpu_gui.log")
print(stdout.read().decode())

ssh.close()
