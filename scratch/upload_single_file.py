import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.0.220", username="xilinx", password="xilinx", timeout=10)
sftp = ssh.open_sftp()
sftp.put(r"D:\QGPU\pynq_board_package\qgpu_board.py", "/home/xilinx/pynq_board_package/qgpu_board.py")
sftp.close()
ssh.close()
print("qgpu_board.py updated on board.")
