import matplotlib.pyplot as plt
import json

fileInfo = json.load(open("results.json"))

sList, iList, rList = [], [], []

for i, r in fileInfo:
    sList.append(1024-i-r)
    iList.append(i)
    rList.append(r)

indexes = tuple(i for i in range(len(fileInfo)))

plt.plot(indexes, sList, label="Susceptible")
plt.plot(indexes, iList, label="Infected")
plt.plot(indexes, rList, label="Recovered")

plt.xlabel("Time Stamp")
plt.ylabel("Persons")

plt.title("SIR")
plt.legend()
plt.show()