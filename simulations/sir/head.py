import json

# same parameter for all simulation cases
def info(num):
    inputs = []

    initI = 1
    gridSize = (32, 32)
    toroidal = True
    dieOut = 64
    SIRProbabilityRanges = None
    SIRProbability = (0.2, 0.4, 0)

    for i in range(num):
        inputs.append((initI, gridSize, toroidal, dieOut, SIRProbabilityRanges, SIRProbability))
    
    return inputs, (dieOut,)


def organize(answers, meta):
    rounds = meta[0]

    averaged = [(0,0) for _ in range(rounds)]
    n = 0

    # adding up all answers
    for answer in answers:
        timeStamp = 0
        for infected, recovered in answer:
            averaged[timeStamp][0] += infected
            averaged[timeStamp][1] += recovered
            timeStamp += 1
        n += 1

    # and divid everything to get the average value
    for i in range(rounds):
        averaged[i][0] /= n
        averaged[i][1] /= n

    return averaged


def saveJSON(organizedAnswer):
    return organizedAnswer