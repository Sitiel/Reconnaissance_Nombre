import connexion
import six
from swagger_server.models.data_train import DataTrain  # noqa: E501
from swagger_server import util

from swagger_server.database import db
from swagger_server.algorithmes.kmeans import findUsingKMeans
from swagger_server.algorithmes.bayesienne import findUsingBaye
from swagger_server.algorithmes.neural import NeuralNet

import swagger_server.algorithmes.utile

import csv
import random


def add_data(dataTrain):  # noqa: E501
    """Add a train data in database

    Add a train data in database  # noqa: E501

    :param dataTrain: Data information
    :type dataTrain: dict | bytes

    :rtype: None
    """
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

    data = []

    with open('data.csv', 'r') as csvfile:
        i = 0
        s = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in s:
            i += 1
            if i == 1:
                continue
            data.append(list(map(int, row[1:])))

    n = NeuralNet(4, 4, 10, 1, 0.8)
    random.shuffle(data)
    for i in range(10000):
        print("Epoch :", i)
        # random.shuffle(data)
        n.train([t[:4] for t in data], [int(t[4])-1 for t in data])


    for test in testData:
        resultK = findUsingKMeans([t["data"] for t in trainData], [t["solution"] for t in trainData], test['data'],
                             swagger_server.algorithmes.utile.distValue)


        resultB = findUsingBaye([t["data"] for t in trainData], [t["solution"] for t in trainData], test['data'])

        resultN = n.guess(test['data'])


        s = int(test["solution"])

        matrixK[s][resultK] += 1
        matrixB[s][resultB] += 1
        matrixN[s][resultN] += 1


    db.addMatrix("kmeans", matrixK)
    db.addMatrix("bayesienne", matrixB)
    db.addMatrix("neural", matrixN)

    return 'success'
