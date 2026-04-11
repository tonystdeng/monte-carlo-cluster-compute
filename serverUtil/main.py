# distrobute simulations sftp
# intereact with heap.py's info function for parameters
# ssh into cluster computers and fun the cluster program
# collect the console output of cluster program
# give that output mentioned above to the orgnize funciton in head.py
# give the orgnized data into the saveJSON function and get a json file
# save the json file which marks the end of the comput session


import paramiko

# Open a transport
host,port = "debian-node14",22
transport = paramiko.Transport((host,port))

# Auth    
username,password = "node14","psw"
transport.connect(None,username,password)

# Go!    
sftp = paramiko.SFTPClient.from_transport(transport)


filepath = "/home/foo.jpg"
localpath = "/home/pony.jpg"
sftp.put(localpath,filepath,)

# Close
if sftp: sftp.close()
if transport: transport.close()
