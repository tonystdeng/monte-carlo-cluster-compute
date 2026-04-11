import paramiko
import os

import clusterInfo as info

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for i in range(info.clusterNum):
    client.connect(hostname=info.hostnames[i], username=info.usernames[i], password=info.passwords[i])

    homePath = "/home/" + str(info.usernames[i])

    stdin, stdout, stderr = client.exec_command(f"mkdir -p {homePath}/ClusterProgram/Programs")
    print(stdout.read().decode())
    print(stderr.read().decode())

    sftp = client.open_sftp()
    sftp.put(os.path.dirname(os.path.abspath(__file__)) + "/cluster.py", homePath + "/ClusterProgram/Cluster.py")
    sftp.close()

    client.close()