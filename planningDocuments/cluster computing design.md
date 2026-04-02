

| Program Type | Definition | Placement & Creation & Trigger | Main Functionality & Possible Code Divisions  |
| :---- | :---- | :---- | :---- |
| mp | Manage program/ Main logic | Remain on hc all time, no change unless updates, run by pc to start the whole session. | Move clp\&cop to clusters. SSH into clusters. Give parameters(from hp). Collect results by reading cluster console(to hp), and return processed data to pc(if any). |
| clp | Cluster program | Remain on cc all time, no change unless updates, run by mp | Run cop and manage multi-core Run by mp, given parameters and give it to cop Print out cop’s result for mp to collect |
| hp | Head program | Received by pc ssh, call by mp | Give parameters to the cluster(ask from mp). Receive(from mp), organize, process, then store/return(to mp) data. |
| cop | Compute program | Received by pc ssh, call by clp | Receive parameters from clp. Return data for clp to collect. |

