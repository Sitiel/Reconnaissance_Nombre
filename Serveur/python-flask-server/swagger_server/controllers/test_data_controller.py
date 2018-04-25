import connexion
import six

import connexion
from swagger_server.algorithmes.kmeans import findUsingKMeans
from swagger_server.algorithmes.bayesienne import findUsingBaye, trainBaye
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

    tmp = db.getAllDataTrain()
    random.shuffle(tmp)
    trainBaye([t["data"] for t in tmp], [t["solution"] for t in tmp])

    resultK = findUsingKMeans([t["data"] for t in trainData], [t["solution"] for t in trainData], image['data'],
                             swagger_server.algorithmes.utile.distValue)


    resultB = findUsingBaye(image['data'], [-9, 31, 3, -6, -1, -10, 1, -10, -2, 4, 2, -8, -5, 47, 3, 31, 0, -9, 0, 0, 3, 43, 41, -1, 3, 16, 88, 10, -6, -5, -2, 20, 17, 45, 38, 4, 2, 44, 33, -1, -8, -4, 9, -2, -6, 19, 0, 2])


    if connexion.request.is_json:
        image = Data.from_dict(connexion.request.get_json())  # noqa: E501
    return {"kmeans": resultK, 'baye': resultB, 'neural': -1}