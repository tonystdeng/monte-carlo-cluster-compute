import numpy as np
import random
import util
import sys
import json

class SimulationGridBase:
    def __init__(self, initI: int = 1, gridSize: tuple[int, int] = (32, 32), useGridDiagnal: bool = True, toroidal: bool = True,# dieOut: float = 0.3,
                    SIRProbabilityRanges: tuple[tuple[float, float], tuple[float, float], tuple[float, float]] = None,
                    SIRProbability: tuple[float, float, float] = None
                    ):
        # scalars
        self.time = 0
        self.T = gridSize[0] * gridSize[1]
        self.peakHistory = [(0,0)]
        self.useGridDiagnal = useGridDiagnal
        self.toroidal = toroidal
        
        # matrix init
        self.gridSize = gridSize
        self.currentCondition = np.zeros(gridSize, dtype=int)# SIR(susceptable-0, infected-1, recovered-2)

        # select initial infected
        self.initI = initI
        while initI > 0:
            selectedPos = tuple(random.randint(0, gridSize[i] - 1) for i in (0, 1))
            if self.currentCondition[selectedPos[0]][selectedPos[1]] == 0:
                initI -= 1
                self.currentCondition[selectedPos[0]][selectedPos[1]] = 1
        self.deltaInfected = self.currentCondition.copy()
        self.history = [self.currentCondition.tolist()]

        # probability (0~1)
        assert SIRProbabilityRanges or SIRProbability, "Needs to input atleast one of SIRProbability and SIRProbabilityRanges"
        assert not (SIRProbabilityRanges and SIRProbability), "Needs to only input one of SIRProbability and SIRProbabilityRanges"
        if SIRProbabilityRanges:
            self.SIRProbability = SIRProbabilityRanges
            self.SIRProbabilityIsRange = True
        else:
            self.SIRProbability = SIRProbability
            self.SIRProbabilityIsRange = False


    def update(self):
        new = self.currentCondition.copy()
        for i in range(self.gridSize[0]):
            for j in range(self.gridSize[1]):
                neighborCounts = util.neighborCounts(self.currentCondition.copy(), i, j, self.toroidal)

                # manage probability based on neighbor count
                changeProb = self.SIRProbability[neighborCounts["self"]]
                if self.SIRProbabilityIsRange:
                    changeProb = random.uniform(*changeProb)
                if neighborCounts["self"] == 0:
                    changeProb = util.getInfectionProb(changeProb,neighborCounts[1])

                #execute
                if random.random() < changeProb:
                    new[i][j] += -2 if new[i][j] == 2 else 1
                    if new[i][j] == 1: self.deltaInfected[i][j] = 1

        # update changes
        self.time += 1
        self.history.append(new.tolist())
        self.currentCondition = new
        havePeak = self.checkIPeak()
        dying = self.checkDie()

        return new, havePeak, dying


    def runUntilDie(self):
        while True:
            new, havePeak, dying = self.update()
            if dying:
                self.save()
                self.saveVis()
                return


    def checkDie(self):
        return self.time == 100


    def checkIPeak(self):
        iCount = np.count_nonzero(self.currentCondition.flat == 1)
        if iCount > self.peakHistory[-1][1]:
            self.peakHistory.append((self.time, iCount))
            return True
        return False
                

    def save(self):
        saves = {"peaks": self.peakHistory, "history": self.history}
        file = open("results.json", "w")
        json.dump(saves, file, indent=2)


    def saveVis(self):
        txt = f"{self.time}:\n"
        for i in range(self.time):
            txt+=f"time: {i}, count: {util.countMatrix(self.history[i])}\n"
            for x in self.history[i]:
                for y in x:
                    txt+=f"{y},"
                txt+="\n"
        open("hi.txt","w").write(txt)