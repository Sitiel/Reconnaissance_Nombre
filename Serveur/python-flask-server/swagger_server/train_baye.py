from algorithmes.tabou import tabouCalcul
from algorithmes.bayesienne import findUsingBaye, trainBaye
from database import db
from algorithmes.utile import centrageSolo
import random

def evaluateBayesienne(hyperparameters):
    global testData
    succes = 0
    for data in testData:
        find = findUsingBaye(centrageSolo(data["data"], 6, 8), hyperparameters)
        succes += 1 if find == int(data["solution"]) else 0
    return succes

def trainBayesienne():
    tmp = db.getAllDataTrain()
    data = [centrageSolo(t['data'], 6, 8) for t in tmp]
    trainBaye(data, [t["solution"] for t in tmp])
    tabouCalcul(48, evaluateBayesienne)


testData = db.getAllDataTest()
random.shuffle(testData)
trainBayesienne()