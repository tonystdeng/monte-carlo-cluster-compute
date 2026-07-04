import paramiko
import os
import sys
import asyncio
import json
import warnings
from datetime import datetime
import importlib.util

import clusterInfo as info
import util

# resets cluster assets:
import init
print("Progress Report: Cluster assets updated through ssh to all clusters.\n")


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
    util.sftp_put_folder(sftp,simulationPath,destination)
    
    sftp.close()
client.close()
print("Progress Report: Simulation programs uploaded through ssh to all clusters.\n")


# intereact with heap.py's info function for parameters
spec = importlib.util.spec_from_file_location(
    "head",
    simulationPath + "/head.py"
)
head = importlib.util.module_from_spec(spec)
spec.loader.exec_module(head)

parameters, metaInfo = head.info(simulationNumber)


# ssh into cluster computers and run the cluster program
async def runCluster(index, parameters, metaInfo):
    # connect
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=info.hostnames[index], username=info.usernames[index], password=info.passwords[index])

    # run cluster program with parameter in json format, the simulation name, and command to organize or not
    inputs = json.dumps([parameters, metaInfo])
    clusterProgramPath = f"/home/{str(info.usernames[index])}/{info.mainFolderName}/{info.clusterProgramName}"
    stdin, stdout, stderr = client.exec_command(f"{info.pythonTriggerCommand} \"{clusterProgramPath}\" \"{inputs}\" \"{simulationName}\"")
    #print("Possible errors will be printed here:", stderr.read().decode(), )

    # decode returns in text that should also be json formate
    returns = stdout.read().decode()
    return json.loads(returns)


# collect the console output of cluster program
async def runClusters(parameters, metaInfo):
    # run all servers on sync with async, each with a sliced part of parameters
    results = await asyncio.gather(*(runCluster(i, parameters[i*simulationPerCluster:(i+1)*simulationPerCluster], metaInfo) for i in range(info.clusterNum)))
    return results

# and run that computation
print("Computation started...\n")
results = asyncio.run(runClusters(parameters, metaInfo))
print("Computation completed, orgnizing outputs...\n")

# give that output mentioned above to the orgnize funciton in head.py
orgnizedData = head.organize(results, metaInfo)
# give the orgnized data into the saveJSON function and get a json file
orgnizedDataJSON = head.saveJSON(orgnizedData)
# save the json file under results/simulationName folder
clusterHeadPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("Orgnized, saving.\n")
saveDir = f"{clusterHeadPath}/results/{simulationName}"
try:
    os.makedirs(saveDir)
except FileExistsError:pass
fileDir = f"{saveDir}/{datetime.now()}.json"
with open(fileDir, "w") as file:
    json.dump(orgnizedDataJSON, file)
#which marks the end of the comput session

print(f"File saved to {fileDir}, program completes successfully.")