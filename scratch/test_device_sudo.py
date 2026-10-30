import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.0.220", username="xilinx", password="xilinx", timeout=10)

code = """
import pynq
import pynq.pl_server.embedded_device
print('Devices with sudo:', pynq.Device.devices)
"""
stdin, stdout, stderr = ssh.exec_command(f"echo xilinx | sudo -S /usr/local/share/pynq-venv/bin/python3 -c \"{code}\"")
print(stdout.read().decode())
print("STDERR:", stderr.read().decode())
ssh.close()
