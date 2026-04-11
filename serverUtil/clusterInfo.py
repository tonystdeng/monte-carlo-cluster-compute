clusterNum = 2

avalibleIndex = [14,15] # [i for i in range(16)]

hostnames = [f"debian-node{i}" for i in avalibleIndex]

usernames = [f"node{i}" for i in avalibleIndex]

passwords = ["psw" for _ in avalibleIndex]

#file system names settings
mainFolderName = "ClusterProgram"
programsFolderName = "Programs"
clusterProgramName = "Cluster.py"
