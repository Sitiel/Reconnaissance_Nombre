from algorithmes.tabou import tabouCalcul
from algorithmes.bayesienne import findUsingBaye, trainBaye
from database import db
from algorithmes.utile import centrageSolo
import random
import copy

def evaluateBayesienne(hyperparameters):
    global testData
    succes = 0
    for data in testData:
        find = findUsingBaye(["data"], hyperparameters)
        succes += 1 if find == int(data["solution"]) else 0
    return succes

def trainBayesienne():
    tmp = db.getAllDataTrain()
    data = [t['data'] for t in tmp]
    trainBaye(data, [t["solution"] for t in tmp])
    tabouCalcul(48, evaluateBayesienne)

def dataToLargeurLongueur(data):
    for i in range (len(data)):
        newData=[0 for j in range (14)]
        for j in range(len(data[i])):
            toAdd=0
            if data[i]['data'][j]==1:
                toAdd=1
            newData[j%6]+=toAdd
            newData[6+int(j/6)]+=toAdd
        data[i]['data']=copy.deepcopy(newData)


testData = db.getAllDataTest() + db.getAllDataTrain()

dataToLargeurLongueur(testData)
random.shuffle(testData)
trainBayesienne()