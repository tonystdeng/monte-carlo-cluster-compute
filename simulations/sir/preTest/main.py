from SimulationGridBase import *

initI = 1
gridSize = (32, 32)
useGridDiagnal = True
toroidal = True
SIRProbability = (0.2, 0.4, 0)

pendemic = SimulationGridBase(initI, gridSize, useGridDiagnal, toroidal, SIRProbability=SIRProbability)
pendemic.runUntilDie()
