import numpy as np
import random
import util
import json

class SIRGrid:
    def __init__(self, initI: int = 1, gridSize: tuple[int, int] = (32, 32), toroidal: bool = True, dieOut: int = 64,
                    SIRProbabilityRanges: tuple[tuple[float, float], tuple[float, float], tuple[float, float]] = None,
                    SIRProbability: tuple[float, float, float] = None
                    ):
        # scalars
        self.time = 0
        self.T = gridSize[0] * gridSize[1]
        self.toroidal = toroidal
        self.dieOut = dieOut
        
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
        self.history = [self.checkSIR()[1:]]

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
        # havePeak = self.checkIPeak()
        self.currentCondition = new
        self.history.append(self.checkSIR()[1:])
        dying = self.checkDie()

        return dying


# function to check the overall sir info over one time stamp
    def checkSIR(self):
        susceptible = 0
        infected = 0
        recovered = 0
        for i in range(self.gridSize[0]):
            for j in range(self.gridSize[1]):
                if self.currentCondition[i][j] == 0:
                    susceptible += 1
                elif self.currentCondition[i][j] == 1:
                    infected += 1
                else:
                    recovered += 1
        return susceptible, infected, recovered


    def runUntilDie(self, returning = True, save = False, saveVis = False):
        while True:
            dying = self.update()
            if dying:
                if returning: return self.history
                if save: self.save()
                if saveVis: self.saveVis()
                return


    def checkDie(self):
        return self.time == self.dieOut


    # def checkIPeak(self):
    #     iCount = np.count_nonzero(self.currentCondition.flat == 1)
    #     if iCount > self.peakHistory[-1][1]:
    #         self.peakHistory.append((self.time, iCount))
    #         return True
    #     return False
                

    def save(self):
        file = open("results.json", "w")
        json.dump(self.history, file)
        file.close()


    def saveVis(self):
        txt = f"{self.time}:\n"
        for i in range(self.time):
            txt+=f"time: {i}, count: {util.countMatrix(self.history[i])}\n"
            for x in self.history[i]:
                for y in x:
                    txt+=f"{y},"
                txt+="\n"
        open("resultsVis.txt","w").write(txt)