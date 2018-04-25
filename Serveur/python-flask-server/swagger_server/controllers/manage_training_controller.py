import connexion
import six
from swagger_server.models.data_train import DataTrain  # noqa: E501
from swagger_server import util

from swagger_server.database import db
from swagger_server.algorithmes.kmeans import findUsingKMeans
from swagger_server.algorithmes.bayesienne import findUsingBaye, trainBaye
from swagger_server.algorithmes.neural import NeuralNet
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
                             swagger_server.algorithmes.utile.distValue)

    trainBaye([centrageSolo(t["data"], 6, 8) for t in trainData], [t["solution"] for t in trainData])
    resultB = findUsingBaye(centrageSolo(dataTrain['data'], 6, 8),
                            [-4, -17, 12, 14, 39, -13, 3, 19, 7, -13, -6, 23, 39, 21, 11, 1, 23, 15, -19, 36, 0, 29,
                             -19, -5, 50, 11, 36, 7, 14, 3, -13, 34, 34, 20, -8, 6, 18, 15, 26, 13, 11, 4, 17, 9, 34,
                             -4, 1, 2])


    #We had the result to their respectives matrices
    matrixK = db.getMatrix("kmeans")
    matrixB = db.getMatrix("bayesienne")
    matrixN = db.getMatrix("neural")
    s = int(dataTrain["solution"])

    matrixK[s][resultK] += 1
    matrixB[s][resultB] += 1
    #matrixN[s][resultN] += 1

    db.addMatrix("kmeans", matrixK)
    db.addMatrix("bayesienne", matrixB)
    db.addMatrix("neural", matrixN)

    #We insert the new data inside the database
    db.insertDataTrain(dataTrain)

    if connexion.request.is_json:
        dataTrain = DataTrain.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


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


    tmp = db.getAllDataTrain()
    trainBaye([centrageSolo(t["data"], 6, 8) for t in tmp], [t["solution"] for t in tmp])



    n = NeuralNet(48, 10, 30, 2, 0.1)
    for i in range(100):
        print("Epoch :", i)
        n.train([centrageSolo(t["data"], 6, 8) for t in trainData], [t["solution"] for t in trainData])

    for test in testData:
        resultK = findUsingKMeans([t["data"] for t in trainData], [t["solution"] for t in trainData], test['data'],
                             swagger_server.algorithmes.utile.distValue)


        resultB = findUsingBaye(centrageSolo(test["data"], 6, 8) ,
                                [-4, -17, 12, 14, 39, -13, 3, 19, 7, -13, -6, 23, 39, 21, 11, 1, 23, 15, -19, 36, 0, 29,
                                 -19, -5, 50, 11, 36, 7, 14, 3, -13, 34, 34, 20, -8, 6, 18, 15, 26, 13, 11, 4, 17, 9,
                                 34, -4, 1, 2])

        resultN = n.guess(centrageSolo(test['data'], 6, 8))


        s = int(test["solution"])

        matrixK[s][resultK] += 1
        matrixB[s][resultB] += 1
        matrixN[s][resultN] += 1


    db.addMatrix("kmeans", matrixK)
    db.addMatrix("bayesienne", matrixB)
    db.addMatrix("neural", matrixN)

    return 'success'
