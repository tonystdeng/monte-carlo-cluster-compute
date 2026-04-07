import paramiko

key = "/home/head/.ssh/id_ed25519"
path_of_transfer="path" 

def MakeFolder(host, user, key, path_of_transfer, max_node):
    for node in range(0, max_node+1): #starts from 0 (0-15)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(
                hostname=host+str(node),
                username=user+str(node),
                key_filename=key
            )

            stdin, stdout, stderr = ssh_client.exec_command("sudo rmdir /home/cc") 
            print(stdout.read().decode())
            print(stderr.read().decode())           

        except Exception as error:
            print(f"FAILED ON NODE {node}: {error}")
        finally:
            ssh_client.close()




MakeFolder("debian-node", "node", key, path_of_transfer, 15)