from collections import Counter


def findUsingKMeans(data, solutions, toFind, distanceFunction, k=3):
    # Get the k nearest point
    nearestPoints = sorted(data, key=lambda r: distanceFunction(r, toFind))[:k]
    # Return the majority in the nearest points
    return max([(k, v) for k, v in Counter([solutions[data.index(v)] for v in nearestPoints]).items()], key=lambda x: x[1])[0]


def findMultipleUsingKMeans(data, solutions, toFinds, distanceFunction, k=3):
    # K-means for multiples values
    return [findUsingKMeans(data, solutions, i, distanceFunction, k) for i in toFinds]


def findImageUsingKMeans(data, solutions, toFind, distanceFunction, k=3):
    # Return the nearest point
    return sorted(data, key=lambda r: distanceFunction(r, toFind))[:k]
