# context:
# runned by main.py through ssh by "python cluster.py json([parameters, metaInfo]) simulationName"
# simulation avalible in the programs folder in the same directory

import sys
import json
import os
from concurrent.futures import ProcessPoolExecutor
import clusterInfo as info

# analysis parameters
_, parameters, simulationName = sys.argv
parameters, metaInfo = json.loads(parameters)
simulationPath = f"{os.path.dirname(os.path.abspath(__file__))}/{simulationName}"

# actuall calculation
compute = __import__(simulationPath+"/compute.py")
with ProcessPoolExecutor() as executor:
    results = list(executor.map(compute.compute, parameters))

# orgnize answer if needed
if info.clusterOrganize:
    head = __import__(simulationPath+"/head.py")
    results = head.organize(results, metaInfo)

# return values as console output
print(json.dumps(results))