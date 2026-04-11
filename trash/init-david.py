import paramiko

KEY = "/home/head/.ssh/id_ed25519"
HOME_PATH = "/home" 
HOST = "debian-node"
USER = "node"
CLUSTER_DOT_PY = "/home/.../Cluster.py" # REPLACE THIS WITH THE LOCATION OF CLUSTER.PY

#Path starts at /home/nodeXX. Do not include that in folderPath
#EXAMPLE: create a folder at /home/nodeXX/ClusterProgram
#   folderPath = "/ClusterProgram"
#   MakeFolder(HOST, USER, KEY, "/ClusterProgram", 15)

def MakeFolder(host, user, key, folderPath, max_node):
    for node in range(0, max_node+1): #starts from 0 (0-15)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(
                hostname=host+str(node),
                username=user+str(node),
                key_filename=key
            )

            nodePath = HOME_PATH + "/node" + str(node)

            stdin, stdout, stderr = ssh_client.exec_command("sudo mkdir " + nodePath + folderPath) 
            print(stdout.read().decode())
            print(stderr.read().decode())           

        except Exception as error:
            print(f"FAILED ON NODE {node}: {error}")
        finally:
            ssh_client.close()



#Path starts at /home/nodeXX. Do not include that in transferPath
def TransferFiles(host, user, key, file, transferPath, max_node):
    for node in range(0, max_node+1): #starts from 0 (0-15)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(
                hostname=host+str(node),
                username=user+str(node),
                key_filename=key
            )

            nodePath = HOME_PATH + "/node" + str(node)

            sftp = ssh_client.open_sftp()
            sftp.put(file, nodePath + transferPath)
            sftp.close()

        except Exception as error:
            print(f"FAILED ON NODE {node}: {error}")
        finally:
            ssh_client.close()


#Create a folder "ClusterProgram" with a folder "Programs" and a file "Cluster.py" inside
MakeFolder(HOST, USER, KEY, "/ClusterProgram", 15)
MakeFolder(HOST, USER, KEY, "/ClusterProgram/Programs", 15)
TransferFiles(HOST, USER, KEY, CLUSTER_DOT_PY, "/ClusterProgram/Cluster.py", 15)
