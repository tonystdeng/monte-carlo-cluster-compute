import paramiko
import os
import sys
import asyncio
import json
import warnings
from datetime import datetime

import clusterInfo as info

_, simulationName, simulationNumber = sys.argv

# if user inputed a valid folder path
if os.path.isdir(simulationName):
    simulationPath = simulationName
    simulationName = os.path.basename(simulationPath)
# if only a name is inputed therefore assumed to be avalible in the simulations folder
else:
    clusterHeadPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    simulationPath = clusterHeadPath + "/simulations/" + simulationName
    if not os.path.isdir(simulationPath):# if there are no such folder
        raise ModuleNotFoundError("Simulation Not Found")

# prepare numbers of simulations
simulationNumber = int(simulationNumber)
if simulationNumber % info.clusterNum:
    simulationNumber -= simulationNumber % info.clusterNum
    warnings.warn(f"Simulation Number Not Divisable By Cluster Number, Simulation Number Shortened To {simulationNumber}")
simulationPerCluster = int(simulationNumber/info.clusterNum)


# distrobute simulations sftp
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for i in range(info.clusterNum):
    destination = f"/home/{str(info.usernames[i])}/{info.mainFolderName}/{info.programsFolderName}/{simulationName}"

    client.connect(hostname=info.hostnames[i], username=info.usernames[i], password=info.passwords[i])

    # deleting duplicates if any
    client.exec_command(f"rm -rf {destination}")

    sftp = client.open_sftp()
    sftp.put(simulationPath, destination)
    
    sftp.close()
    client.close()


# intereact with heap.py's info function for parameters
head = __import__(simulationPath + "/head.py")
parameters, metaInfo = head.info(simulationNumber)


# ssh into cluster computers and run the cluster program
async def runCluster(index, parameters, metaInfo):
    # connect
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=info.hostnames[index], username=info.usernames[index], password=info.passwords[index])

    # fun cluster program with parameter in json format, the simulation name, and command to organize or not
    inputs = json.dumps([parameters, metaInfo])
    clusterProgramPath = f"/home/{str(info.usernames[index])}/{info.mainFolderName}/{info.clusterProgramName}"
    stdin, stdout, stderr = client.exec_command(f"python {clusterProgramPath} {inputs} {simulationName}")
    print(stderr.read().decode())

    # decode returns in text that should also be json formate
    return json.loads(stdout.read().decode())


# collect the console output of cluster program
async def runClusters(parameters, metaInfo):
    # run all servers on sync with async, each with a sliced part of parameters
    results = await asyncio.gather(*(runCluster(i, parameters[i*simulationPerCluster:(i+1)*simulationPerCluster], metaInfo) for i in range(info.clusterNum)))
    return results


# give that output mentioned above to the orgnize funciton in head.py
results = asyncio.run(runClusters(parameters, metaInfo))
orgnizedData = head.organize(results, metaInfo)
# give the orgnized data into the saveJSON function and get a json file
orgnizedDataJSON = head.saveJSON(orgnizedData)
# save the json file under results/simulationName folder
clusterHeadPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
saveDir = f"{clusterHeadPath}/results/{simulationName}"
try:
    os.makedirs(saveDir)
except OSError:pass
with open(f"{saveDir}/{datetime.now()}.json") as file:
    file.write(orgnizedDataJSON)
#which marks the end of the comput session