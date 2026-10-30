import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.0.220", username="xilinx", password="xilinx", timeout=10)

code = """
import pynq
import pynq.pl_server.embedded_device
print('Subclasses after embedded_device:', pynq.pl_server.device.DeviceMeta._subclasses)
print('Devices:', pynq.Device.devices)
"""
stdin, stdout, stderr = ssh.exec_command(f"/usr/local/share/pynq-venv/bin/python3 -c \"{code}\"")
print(stdout.read().decode())
print("STDERR:", stderr.read().decode())
ssh.close()
