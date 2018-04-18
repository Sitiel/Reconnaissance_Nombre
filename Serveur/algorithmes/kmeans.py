import csv
import random
import copy
from beautifultable import BeautifulTable
from collections import Counter



data = []
otherData = []

def distance(a, b, d):
    return sum([abs(a[i] - b[i]) for i in range(4)])

def findUsingKMeans(data, toFind, k = 5):
    nearestPoints = sorted(data, key=lambda r: distance(r, toFind, 1))[:k]
    return max([(k, v) for k, v in Counter([i[4] for i in nearestPoints]).items()], key=lambda x: x[1])[0]

def findMultipleUsingKMeans(data, toFinds, k=5):
    return [findUsingKMeans(data, i, k) for i in toFinds]

with open('data.csv', 'r') as csvfile:
    i = 0
    s = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in s:
        i += 1
        if i == 1:
            continue
        data.append(list(map(int, row[1:])))




random.shuffle(data)
trainData = data[:int(len(data) * 0.75)]
testData = data[int(len(data) * 0.75):]

result = findMultipleUsingKMeans(trainData, testData)

print(result)

print("Accuracy :", sum([1 for i,v in enumerate(result) if v == testData[i][4]])/len(testData))
