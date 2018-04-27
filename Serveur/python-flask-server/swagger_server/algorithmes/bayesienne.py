#Bayesienne
import math
import random
import copy

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
        return moyenne
    pi = 3.1415926
    denom = (2 * pi * var) ** .5
    num = math.exp(-(float(x) - float(moyenne)) ** 2 / (2 * var))
    return num / denom

possibilities = 0
classifieur = []

def trainBaye (data, solutions):
    global possibilities
    global classifieur
    possibilities = 10
    classifieur = [[] for i in range(possibilities)]
    for possibility in range(possibilities):
        # Get all data of possibility
        currentData = [d for index, d in enumerate(data) if solutions[index] == possibility]
        # For all pixels
        for j in range(len(currentData[0])):
            # calculate probability
            moy = sum([x[j] for x in currentData]) / len(currentData)
            ecartttype = math.sqrt(sum([(x[j] - moy) * (x[j] - moy) for x in currentData]) / len(currentData))
            classifieur[possibility] += [moy, ecartttype]


def findUsingBaye(toFind, hyperparameters):
    global possibilities
    global classifieur
    proba = [1 for i in range(possibilities)]
    for i in range(possibilities):
        # For all pixels
        for j in range(len(toFind)):
            r = hyperparameters[j*2+1] + loiNormale(toFind[j], classifieur[i][j*2], classifieur[i][j*2+1])
            if r == 0:
                continue
            proba[i] *= pow(r, hyperparameters[j*2])
    return proba.index(max(proba))
