import os
import paramiko

HOST = "192.168.0.220"
USER = "xilinx"
PASS = "xilinx"
LOCAL_DIR = r"D:\QGPU\pynq_board_package"
REMOTE_DIR = "/home/xilinx/pynq_board_package"

def upload_folder():
    print(f"Connecting to {HOST} via SSH/SFTP...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASS, timeout=10)
    sftp = ssh.open_sftp()

    def mkdir_p(remote_path):
        dirs = []
        path = remote_path
        while len(path) > 1:
            dirs.append(path)
            path, _ = os.path.split(path)
        for d in reversed(dirs):
            try:
                sftp.stat(d)
            except IOError:
                try:
                    sftp.mkdir(d)
                except Exception:
                    pass

    mkdir_p(REMOTE_DIR)

    for root, dirs, files in os.walk(LOCAL_DIR):
        rel = os.path.relpath(root, LOCAL_DIR)
        rem_sub = os.path.join(REMOTE_DIR, rel).replace("\\", "/")
        mkdir_p(rem_sub)
        for f in files:
            loc_f = os.path.join(root, f)
            rem_f = os.path.join(rem_sub, f).replace("\\", "/")
            print(f"Uploading: {rel}/{f} -> {rem_f} ...")
            sftp.put(loc_f, rem_f)

    sftp.close()
    stdin, stdout, stderr = ssh.exec_command(f"chmod +x {REMOTE_DIR}/*.sh {REMOTE_DIR}/*.py")
    stdout.channel.recv_exit_status()
    print("All files uploaded successfully and permissions set.")
    ssh.close()

if __name__ == "__main__":
    upload_folder()
