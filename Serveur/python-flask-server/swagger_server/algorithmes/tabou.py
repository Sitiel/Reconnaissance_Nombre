import random
import copy
import math

def isIn(ltabou, v):
    for l in ltabou:
        found = True
        if l == []:
            continue
        for i, x in enumerate(l):
            if x != v[i]:
                found = False
                break
        if found:
            return True
    return False

def tabouCalcul(variablesCount, evaluate):

    # Hyperparameters
    ltabouSize = 1

    ltabou = [[] for i in range(ltabouSize)]

    current = [1 for i in range(variablesCount)]

    notProgressing = 0
    a = 0
    maxBorne = 100

    currentBest = current
    currentBestValue = -9999999999

    while(notProgressing < 100):
        lVoisins = []
        while len(lVoisins) < 100:
            v = copy.deepcopy(current)
            r = random.randint(0, len(v)-1)
            v[r] = random.randint(0, maxBorne)
            if isIn(ltabou, v) == False:
                lVoisins.append(v)
        newCurrent = []
        best = -99999999999
        for v in lVoisins:
            tmp = evaluate(v)
            if tmp > best:
                best = tmp
                newCurrent = v
        current = newCurrent

        ltabou[a] = current
        a += 1
        a = a % ltabouSize
        print("currentBestValue:", currentBestValue)

        if best > currentBestValue:
            print("best:",best)
            notProgressing = 0
            currentBestValue = best
            currentBest = newCurrent
        notProgressing += 1
    print("Current best :", currentBest, "with", currentBestValue)
    return