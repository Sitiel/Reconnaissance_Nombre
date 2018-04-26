import connexion
import six
from swagger_server.models.data_train import DataTrain  # noqa: E501
from swagger_server import util

from swagger_server.database import db
from swagger_server.algorithmes.kmeans import findUsingKMeans
from swagger_server.algorithmes.bayesienne import findUsingBaye, trainBaye
from swagger_server.algorithmes.neural import NeuralNet
from swagger_server.algorithmes.all import testAll
from swagger_server.algorithmes.utile import centrageSolo

import swagger_server.algorithmes.utile

import csv
import random


def add_data(dataTrain):  # noqa: E501
    """Add a train data in database

    Try to guess first then add it to the confusion matrix

    Add a train data in database  # noqa: E501

    :param dataTrain: Data information
    :type dataTrain: dict | bytes

    :rtype: None
    """
    
    #We get the solution for the 3 algorithms
    trainData = db.getAllDataTrain()

    resultK = findUsingKMeans([t["data"] for t in trainData], [t["solution"] for t in trainData], dataTrain['data'],
                             swagger_server.algorithmes.utile.distValue, k=3)

    trainBaye([centrageSolo(t["data"], 6, 8) for t in trainData], [t["solution"] for t in trainData])
    resultB = findUsingBaye(centrageSolo(dataTrain['data'], 6, 8),
                            [4.14, 46.99, 24.19, 15, 12.04, 9, 15.31, 18, 59.58, 20.99, 61.95, 66.41, 8, 12])

    n = NeuralNet(48, 10, 50, 2, 0.1)
    resultN = n.guess(swagger_server.algorithmes.utile.centrageSolo(dataTrain['data'], 6, 8))

    resultA = testAll(dataTrain['data'], resultK, resultB)

    #We had the result to their respectives matrices
    matrixK = db.getMatrix("kmeans")
    matrixB = db.getMatrix("bayesienne")
    matrixN = db.getMatrix("neural")
    matrixA = db.getMatrix("all")
    s = int(dataTrain["solution"])

    matrixK[s][resultK] += 1
    matrixB[s][resultB] += 1
    matrixN[s][resultN] += 1
    matrixA[s][resultA] += 1

    db.addMatrix("kmeans", matrixK)
    db.addMatrix("bayesienne", matrixB)
    db.addMatrix("neural", matrixN)
    db.addMatrix("all", matrixA)

    #We insert the new data inside the database
    db.insertDataTrain(dataTrain)

    if connexion.request.is_json:
        dataTrain = DataTrain.from_dict(connexion.request.get_json())  # noqa: E501
    return 'success'


def start_train():  # noqa: E501
    """Get Confusion Matrix of all Algorithms

    Get Confusion Matrix of all Algorithms  # noqa: E501


    :rtype: None
    """


    trainData = db.getAllDataTrain()
    testData = db.getAllDataTest()

    matrixK = db.getMatrix("kmeans")
    matrixB = db.getMatrix("bayesienne")
    matrixN = db.getMatrix("neural")
    matrixA = db.getMatrix("all")


    tmp = db.getAllDataTrain()
    trainBaye([centrageSolo(t["data"], 6, 8) for t in tmp], [t["solution"] for t in tmp])



    n = NeuralNet(48, 10, 50, 2, 0.01)
    for i in range(100):
        print("Epoch :", i)
        random.shuffle(trainData)
        n.train([centrageSolo(t["data"], 6, 8) for t in trainData], [t["solution"] for t in trainData])

    cmp = 0
    testData += trainData

    for test in testData:
        print(cmp, "/", len(testData))
        cmp+=1
        random.shuffle(trainData)

        resultK = findUsingKMeans([t["data"] for t in trainData], [t["solution"] for t in trainData], test['data'],
                             swagger_server.algorithmes.utile.distValue, k=3)


        resultB = findUsingBaye(centrageSolo(test["data"], 6, 8) ,
                                [4.14, 46.99, 24.19, 15, 12.04, 9, 15.31, 18, 59.58, 20.99, 61.95, 66.41, 8, 12])

        resultN = n.guess(centrageSolo(test['data'], 6, 8))

        resultA = testAll(test['data'], resultK, resultB)


        s = int(test["solution"])

        matrixK[s][resultK] += 1
        matrixB[s][resultB] += 1
        matrixN[s][resultN] += 1
        matrixA[s][resultA] += 1

        #if resultN != s:
        #    print("Error on ", centrageSolo(test["data"],6,8), "say", resultN, "was", s)


    db.addMatrix("kmeans", matrixK)
    db.addMatrix("bayesienne", matrixB)
    db.addMatrix("neural", matrixN)
    db.addMatrix("all", matrixA)

    return 'success'

def reset_matrix():
    db.removeMatrix()
    return 'success'