import connexion
import six

import connexion
from swagger_server.algorithmes.kmeans import findUsingKMeans
from swagger_server.algorithmes.bayesienne import findUsingBaye, trainBaye
from swagger_server.algorithmes.neural import NeuralNet
from swagger_server.models.data import Data  # noqa: E501
import swagger_server.algorithmes.utile
from swagger_server.database import db
import random


def test_data(image):  # noqa: E501
    """Add a train data in database

    Add a train data in database  # noqa: E501

    :param image: Data information
    :type image: dict | bytes

    :rtype: Solution
    """

    trainData = db.getAllDataTrain()

    resultK = findUsingKMeans([t["data"] for t in trainData], [t["solution"] for t in trainData], image['data'],
                             swagger_server.algorithmes.utile.distValue, k=3)

    trainBaye([swagger_server.algorithmes.utile.centrageSolo(t["data"], 6, 8) for t in trainData], [t["solution"] for t in trainData])

    resultB = findUsingBaye(swagger_server.algorithmes.utile.centrageSolo(image['data'], 6, 8),
                            [7, -10, -9, -10, -18, -15, -2, -19, 16, 20, -15, 37, 4, 35, 7, 36, 27, 16, 26, 8, 31, 10,
                             -18, -15, 0, 2, 34, 18, 15, -6, 5, 31, 65, -4, 44, 27, 9, 5, 28, 30, -4, 11, -2, 1, -7, 13,
                             -5, 7])

    n = NeuralNet(48, 10, 50, 2, 0.1)
    resultN = n.guess(swagger_server.algorithmes.utile.centrageSolo(image['data'],6, 8))

    if connexion.request.is_json:
        image = Data.from_dict(connexion.request.get_json())  # noqa: E501
    return {"kmeans": resultK, 'baye': resultB, 'neural': resultN}