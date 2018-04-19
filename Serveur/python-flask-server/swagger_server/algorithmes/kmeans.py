from collections import Counter


def findUsingKMeans(data, solutions, toFind, distanceFunction, k = 1):
    nearestPoints = sorted(data, key=lambda r: distanceFunction(r, toFind))[:k]
    for i in nearestPoints:
        print("Nearest : ", i, "distance ", distanceFunction(i, toFind))
    return max([(k, v) for k, v in Counter([solutions[i] for i, v in enumerate(nearestPoints)]).items()], key=lambda x: x[1])[0]

def findMultipleUsingKMeans(data, solutions, toFinds, distanceFunction, k=5):
    return [findUsingKMeans(data, solutions, i, distanceFunction, k) for i in toFinds]

