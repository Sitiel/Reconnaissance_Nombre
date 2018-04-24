from algorithmes.tabou import tabouCalcul
from algorithmes.kmeans import findUsingKMeans
from database import db
import random
from algorithmes.utile import distValue

trainData = db.getAllDataTrain()
trainSolutions = [t["solution"] for t in trainData]
trainData = [t["data"] for t in trainData]

def evaluateKmeans(hyperparameters):
    global testData
    global trainData
    global trainSolutions
    succes = 0
    for data in testData:
        find = findUsingKMeans(trainData, trainSolutions, data["data"], distValue)
        succes += 1 if find == int(data["solution"]) else 0
    return succes

def trainKmeans():
    tabouCalcul(48, evaluateKmeans)


testData = db.getAllDataTest()
random.shuffle(testData)
trainKmeans()