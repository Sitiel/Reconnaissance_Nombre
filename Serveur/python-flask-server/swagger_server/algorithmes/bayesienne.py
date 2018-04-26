#Bayesienne
import math
import random

def moyenne(listImage):
    listRetour = []
    for i in range(len(listImage[0])):
        a = [v[i] for v in listImage]
        listRetour.append(sum(a) / len(a))
    return listRetour


def ecartType(listImage, moyenne):
    imageRet = [0 for x in range(len(listImage[0]))]
    for i in range(len(listImage[0])):
        for j in range(len(listImage)):
            imageRet[i] += math.pow(listImage[j][i] - moyenne[i], 2)
    for i in range(len(imageRet)):
        imageRet[i] = math.sqrt(imageRet[i] / len(imageRet))
    return imageRet


def loiNormale(x, moyenne, ecartType):
    var = float(ecartType) ** 2
    if var == 0:
        return 1
    pi = 3.1415926
    denom = (2 * pi * var) ** .5
    num = math.exp(-(float(x) - float(moyenne)) ** 2 / (2 * var))
    return num / denom


def evaluateur(data, solutions, toFind):
    dataSorted = []
    dataEcarType = []
    dataMoyenne = []
    for j in range(10):
        dataSorted.append([v for i, v in enumerate(data) if solutions[i] == j])

    for k in range(len(dataSorted)):
        dataMoyenne.append(moyenne(dataSorted[k]))
        dataEcarType.append(ecartType(dataSorted[k], dataMoyenne[k]))

    bestPercent = 0
    number = -1

    for k in range(len(dataMoyenne)):
        currentPercent = -1
        for j in range(len(dataMoyenne[0])):
            if dataEcarType[k][j] == 0:
                currentPercent *= loiNormale(toFind[j], dataMoyenne[k][j], 1)
            else:
                currentPercent *= loiNormale(toFind[j], dataMoyenne[k][j], dataEcarType[k][j])
        if currentPercent > bestPercent:
            bestPercent = currentPercent
            number = k
    return number

possibilities = 0
classifieur = []

def trainBaye (data, solutions):
    global possibilities
    global classifieur
    possibilities = 10
    classifieur = [[] for i in range(possibilities)]
    for i in range(possibilities):
        currentData = [d for index, d in enumerate(data) if solutions[index] == i]
        for j in range(len(currentData[0])):
            moy = sum([x[j] for x in currentData]) / len(currentData)
            ecartttype = math.sqrt(sum([(x[j] - moy) * (x[j] - moy) for x in currentData]) / len(currentData))
            classifieur[i] += [moy, ecartttype]


def findUsingBaye(toFind, hyperparameters):
    global possibilities
    global classifieur

    proba = [1 for i in range(possibilities)]
    for i in range(possibilities):
        for j in range(len(toFind)):
            proba[i] *= pow(loiNormale(toFind[j], classifieur[i][j * 2], classifieur[i][j * 2 + 1]), hyperparameters[j])

    return proba.index(max(proba))