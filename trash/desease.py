import numpy as np

class SimulationBase:
    def __init__(self, initInfect, popW, popH, beta, gamma, 
                 useDiagnalNeighborhood = True):
        # scalars
        self.time = 0
        self.pop = popW * popH
        self.useDiagnalNeighborhood = useDiagnalNeighborhood
        
        # matrix
        self.currentCondition = np.ndarray((popW, popH))# SIR(susceptable-0, infected-1, recovered-2)
        self.deltaInfected = np.ndarray((popW, popH))

        # updates all time
        self.peakInfect = 0
        self.peakInfectTime = 0

        # probability (0~1)
        self.beta = beta # infection posibility(used combine with neighor)
        self.gamma = gamma # recovery posibility

    
    def checkDieOut(self):
        pass

    def infected(self):
        pass

    def run(self):
        pass