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
from swagger_server.benchmark import benchmark
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
                            [1, 0.2531456233559495, -5, 0.6072957508842917, 1, 0.8977458741334808, 1,
                             0.5315365624049261, 1, 0.5539299829957939, 1, 0.9470958258490086, 1, 1, 13, 1, 1,
                             0.41503558482424896, 1, 0.37175606837229247, 1, 0.20695730675896218, 1, 0.2573449354657006,
                             1, 0.9706451692840014, 1, 0.2596921672325243, 1, 0.8469245175205712, 1,
                             0.12008343338330807, 18, 0.9837415474516443, 1, 0.05673329184999265, 1, 0.9796896851994393,
                             1, 0.015172666264064327, 1, 0.8359529635057672, 26, 1, 1, 0.1298727669076093, 1,
                             0.27935195257637346, 1, 0.3481340354492565, 1, 0.7217607161682704, 39, 1, 1,
                             0.7920877456683918, 1, 0.7364798746584718, 1, 0.3274710844989588, 1, 0.1741058936094959, 1,
                             0.03187456203144079, 1, 0.8169259491127986, 1, 1, 1, 0.7913958139586836, 1,
                             0.8854463253804352, 1, 0.20060822247547672, 1, 0.699886481283334, 20, 0.9564868845194423,
                             1, 0.8071204985915956, 1, 0.04542392705337095, 1, 0.8036952517710982, 1,
                             0.7106628822423792, 1, 0.1505108082468265, 1, 0.12041286403451934, 1, 0.029648460457306403,
                             1, 0.5450252027347883, 1, 1])

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


    #tmp = db.getAllDataTrain()
    #trainBaye([centrageSolo(t["data"], 6, 8) for t in tmp+trainData], [t["solution"] for t in tmp+trainData])

    benchmark.set_data(trainData+testData)

    n = NeuralNet(48, 10, 50, 2, 0.01)
    for i in range(50):
        print("Epoch :", i)
        random.shuffle(trainData)
        n.train([centrageSolo(t["data"], 6, 8) for t in trainData+testData], [int(t["solution"]) for t in trainData+testData])

    cmp = 0

    for test in testData:
        print(cmp, "/", len(testData))
        cmp += 1

        result = benchmark.test_data(test['data'])

        s = int(test["solution"])

        matrixK[s][result['kmeans']] += 1
        matrixB[s][result['baye']] += 1
        matrixN[s][result['neural']] += 1
        matrixA[s][result['all']] += 1


    db.addMatrix("kmeans", matrixK)
    db.addMatrix("bayesienne", matrixB)
    db.addMatrix("neural", matrixN)
    db.addMatrix("all", matrixA)
    return 'success'

def reset_matrix():
    db.removeMatrix()
    return 'success'