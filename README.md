# Monte Carlo Cluster Computing Server

Using multiple low-end computers to form a cluster computing system with mainly ssh communication methods for purpose of performing Monte Carlo Simulations.

More detailed documentations on logics and designs in [this](./documentations/) folder(to be completed).

## How to use
1. Prepare clusters and incluster information: 

    Prepare devices ready for incoming ssh connections, edit variables in [clusterInfo.py](./serverUtil/clusterInfo.py) based on its current example code to update the rest of the programs to adapt to your unique system and clusters.
2. Prepare simulation program:

    Under folder [simulations](./simulations/), create new folder with any name. Include all necessary asset files and the required **head.py** and **computer.py** as explained more detailly in the [documentations](./documentations/) (to be completed).
3. Upload Cluster Util To Clusters:

    Simply run file [init.py](./serverUtil/init.py). Note that this step will be automaticly completed again by other programs in later steps, though it is reccommended for early testing and to check the correct completion of the first step.

4. Process Simulation:

    Run file [mian.py](./serverUtil/main.py) in formate `python main.py <simulation-folder> <simulation-number>`, as it will automate:

    - Step 3 as explained.
    - Upload the simulation explain in step 2 as inputed to all clusters.
    - Prepare and launch a multi-thread execution of the simulations on all clusters with a totle number of times as inputed.
    - Orgnize the answer and export it to `./results` where user can use it as will.

## Potential Future Updates
- Further completion of the [documentations](./documentations/).
- Further optimization and debugging.
- Increase compatibility for more diverse case.