import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("192.168.0.220", username="xilinx", password="xilinx", timeout=10)

ssh.exec_command("cp /home/xilinx/pynq_board_package/run.sh /home/xilinx/run.sh && chmod +x /home/xilinx/run.sh")
ssh.close()
print("Copied run.sh to /home/xilinx/run.sh")
