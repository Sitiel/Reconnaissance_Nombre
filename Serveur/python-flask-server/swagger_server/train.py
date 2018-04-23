from algorithmes.tabou import tabouCalcul
from algorithmes.bayesienne import findUsingBaye
from database import db
import random

def evaluateBayesienne (hyperparameters):

    succes = 0
    for data in testData:
        find = findUsingBaye(data["data"],hyperparameters)
        succes += 1 if find == data["solution"] else 0
    return succes

def trainBayesienne ():
    global testData
    tmp = db.getAllDataTrain()
    random.shuffle(tmp)
    testData = tmp[int(0.75*len(tmp)):]
    tabouCalcul(48, evaluateBayesienne)

trainBayesienne()