import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.0.220", username="xilinx", password="xilinx", timeout=10)

code = """
import pynq.pl_server.device as dev
print('Subclasses:', dev.DeviceMeta._subclasses)
for k, cls in dev.DeviceMeta._subclasses.items():
    try:
        print(cls, 'probe:', cls._probe_())
    except Exception as e:
        print(cls, 'error:', e)
"""
stdin, stdout, stderr = ssh.exec_command(f"/usr/local/share/pynq-venv/bin/python3 -c \"{code}\"")
print(stdout.read().decode())
print("STDERR:", stderr.read().decode())
ssh.close()
