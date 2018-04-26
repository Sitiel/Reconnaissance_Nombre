import six

from swagger_server.algorithmes.kmeans import findUsingKMeans
from swagger_server.algorithmes.bayesienne import findUsingBaye, trainBaye
from swagger_server.algorithmes.neural import NeuralNet
from swagger_server.algorithmes.all import testAll
from swagger_server.models.data import Data  # noqa: E501
import swagger_server.algorithmes.utile
from swagger_server.database import db
import random

class Benchmark:

    def test_data(self, image):  # noqa: E501
        """Add a train data in database

        Add a train data in database  # noqa: E501

        :param image: Data information
        :type image: dict | bytes

        :rtype: Solution
        """

        trainData = db.getAllDataTrain()

        resultK = findUsingKMeans([t["data"] for t in trainData], [t["solution"] for t in trainData], image['data'],
                                swagger_server.algorithmes.utile.distValue)

        trainBaye([swagger_server.algorithmes.utile.centrageSolo(t["data"], 6, 8) for t in trainData], [t["solution"] for t in trainData])

        resultB = findUsingBaye(swagger_server.algorithmes.utile.centrageSolo(image['data'], 6, 8),
                                [4.14, 46.99, 24.19, 15, 12.04, 9, 15.31, 18, 59.58, 20.99, 61.95, 66.41, 8, 12])

        n = NeuralNet(48, 10, 30, 2, 0.1)
        resultN = n.guess(swagger_server.algorithmes.utile.centrageSolo(image['data'],6, 8))

        resultA = testAll(image['data'], resultK, resultB)

        return {"kmeans": resultK, 'baye': resultB, 'neural': resultN, 'all': resultA}


benchmark = Benchmark()