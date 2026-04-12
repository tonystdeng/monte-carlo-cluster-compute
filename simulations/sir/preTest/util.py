import numpy as np

def cropNeighbors(matrix: np.ndarray, x: int, y: int):
    returns = np.empty((3, 3), int)
    for i in range(3):
        mx = x + i - 1
        for j in range(3):
            my = y + j - 1
            returns[i][j] = -1 if 0>mx or mx>matrix.shape[0]-1 or 0>my or my>matrix.shape[1]-1 else matrix[mx][my]
    return returns


def cropNeighborsToroidal(matrix: np.ndarray, x: int, y: int):
    returns = np.empty((3, 3), int)
    for i in range(3):
        mx = x + i - 1
        if mx == matrix.shape[0]: mx = 0
        for j in range(3):
            my = y + j - 1
            if my == matrix.shape[1]: my = 0
            returns[i][j] = matrix[mx][my]
    return returns


def neighborCounts(matrix: np.ndarray, x: int, y: int, toroidal: bool):
    crop = cropNeighborsToroidal(matrix, x, y) if toroidal else cropNeighbors(matrix, x, y)
    info = {"self": int(crop[1][1]), -1: 0, 0: 0, 1: 0, 2: 0}
    crop[1][1] = -2
    for i in crop.flat:
        i = int(i)
        if i == -2: continue
        else: info[i] += 1
    return info


def getInfectionProb(beta, infectionCount):
    return 1 - (1 - beta) ** infectionCount


def countMatrix(matrix):
    num = 0
    for i in matrix:
        for j in i:
            if j == 1:
                num += 1
    return num