import paramiko

key = "/home/head/.ssh/id_ed25519"
file_to_transfer="/home/head/DELETE_THIS_AFTER"
path_of_transfer="path" #Specify where the file will be transferred to. Include the file name, not just directory

def transferFiles(host, user, key, file_to_transfer, path_of_transfer, max_node):
    for node in range(0, max_node+1): #starts from 0 (0-15)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(
                hostname=host+str(node),
                username=user+str(node),
                key_filename=key
            )

            sftp = ssh_client.open_sftp()
            sftp.put(file_to_transfer, path_of_transfer)
            sftp.close()

        except Exception as error:
            print(f"FAILED ON NODE {node}: {error}")
        finally:
            ssh_client.close()




transferFiles("debian-node", "node", key, file_to_transfer, path_of_transfer, 15)