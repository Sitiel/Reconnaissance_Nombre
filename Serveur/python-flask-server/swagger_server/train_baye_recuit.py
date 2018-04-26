from algorithmes.recuit import recuitCalcul
from algorithmes.bayesienne import findUsingBaye, trainBaye
from database import db
from algorithmes.utile import centrageSolo
import random
import copy

def evaluateBayesienne(hyperparameters):
    global testData
    succes = 0
    for data in testData:
        find = findUsingBaye(data['data'], hyperparameters)
        succes += 1 if find == int(data["solution"]) else 0
    return succes

def trainBayesienne():
    tmp = db.getAllDataTrain()
    for i in range(len(tmp)):
        centrageSolo(tmp[i]['data'],6,8)
    data = [t['data']for t in tmp]
    trainBaye(data, [t["solution"] for t in tmp])
    recuitCalcul(14, evaluateBayesienne)

testData = db.getAllDataTest() + db.getAllDataTrain()
for i in range(len(testData)):
    centrageSolo(testData[i]['data'],6,8)
random.shuffle(testData)
trainBayesienne()
