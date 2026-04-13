import paramiko
import os

import clusterInfo as info

# create the ssh client that will be used throughout the automation
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# loop through all clusters
for i in range(info.clusterNum):
    # prepare based on index
    client.connect(hostname=info.hostnames[i], username=info.usernames[i], password=info.passwords[i])
    homePath = "/home/" + str(info.usernames[i])

    # delete old version of cluster main folder and then install new ones
    stdin, stdout, stderr = client.exec_command(f"rm -rf {homePath}/{info.mainFolderName}")
    stdin, stdout, stderr = client.exec_command(f"mkdir -p {homePath}/{info.mainFolderName}/{info.programsFolderName}")

    # transfer cluster.py and its nessesary assist programs
    sftp = client.open_sftp()
    sftp.put(os.path.dirname(os.path.abspath(__file__)) + "/cluster.py", 
             homePath + f"/{info.mainFolderName}/{info.clusterProgramName}")
    sftp.put(os.path.dirname(os.path.abspath(__file__)) + "/clusterInfo.py", 
             homePath + f"/{info.mainFolderName}/clusterInfo.py")
    
    # end
    sftp.close()
    client.close()