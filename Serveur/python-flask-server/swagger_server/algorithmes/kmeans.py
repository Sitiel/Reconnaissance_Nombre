from collections import Counter


def findUsingKMeans(data, solutions, toFind, distanceFunction, k = 3):
    nearestPoints = sorted(data, key=lambda r: distanceFunction(r, toFind))[:k]
    return max([(k, v) for k, v in Counter([solutions[data.index(v)] for v in nearestPoints]).items()], key=lambda x: x[1])[0]

def findMultipleUsingKMeans(data, solutions, toFinds, distanceFunction, k = 3):
    return [findUsingKMeans(data, solutions, i, distanceFunction) for i in toFinds]

def findImageUsingKMeans(data, solutions, toFind, distanceFunction, k = 3):
    return sorted(data, key=lambda r: distanceFunction(r, toFind))[:k]