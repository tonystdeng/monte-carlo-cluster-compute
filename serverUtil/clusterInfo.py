clusterNum = 2

avalibleIndex = [0, 1] # [i for i in range(clusterNum)]

hostnames = [f"debian-node{i}" for i in avalibleIndex]

usernames = [f"node{i}" for i in avalibleIndex]

passwords = ["psw" for _ in avalibleIndex]

#file system names settings
mainFolderName = "ClusterProgram"
programsFolderName = "Programs"
clusterProgramName = "Cluster.py"


# cluster settings
clusterOrganize = True
pythonTriggerCommand = "python3"