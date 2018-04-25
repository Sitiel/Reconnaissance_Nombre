from collections import Counter


def findUsingKMeans(data, solutions, toFind, distanceFunction,hyperparameters):
    k = 1 if hyperparameters[0] < 1 else hyperparameters[0]
    nearestPoints = sorted(data, key=lambda r: distanceFunction(r, toFind, hyperparameters))[:k]
    return max([(k, v) for k, v in Counter([solutions[data.index(v)] for v in nearestPoints]).items()], key=lambda x: x[1])[0]

def findMultipleUsingKMeans(data, solutions, toFinds, distanceFunction, hyperparameters):
    return [findUsingKMeans(data, solutions, i, distanceFunction, hyperparameters) for i in toFinds]

