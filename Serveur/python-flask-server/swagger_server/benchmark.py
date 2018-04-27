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

    def __init__(self):
        trainData = db.getAllDataTrain()+db.getAllDataTest()
        self.kData = [t["data"] for t in trainData]
        self.solutions = [int(t["solution"]) for t in trainData]
        self.trainData = [swagger_server.algorithmes.utile.centrageSolo(t["data"], 6, 8) for t in trainData]
        trainBaye(self.trainData, self.solutions)

    def set_data(self, trainData):
        self.kData = [t["data"] for t in trainData]
        self.solutions = [int(t["solution"]) for t in trainData]
        self.trainData = [swagger_server.algorithmes.utile.centrageSolo(t["data"], 6, 8) for t in trainData]
        trainBaye(self.trainData, self.solutions)

    def test_data(self, image):  # noqa: E501
        """Add a train data in database

        Add a train data in database  # noqa: E501

        :param image: Data information
        :type image: dict | bytes

        :rtype: Solution
        """

        #resultK = findUsingKMeans(self.kData, self.solutions, image,
        #                        swagger_server.algorithmes.utile.distValue)
        resultK = 0

        resultB = findUsingBaye(swagger_server.algorithmes.utile.centrageSolo(image, 6, 8),
                                [1, 1, 1, 0.09862885458351156, 1, 1, 1, 0.4700416302561873, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                 1, 1, 1, 1, 0.2678075596232564, 1, 1, 1, 1, 1, 0.06921773190651959, 1, 1, 1,
                                 0.5633503668432782, 1, 0.1794706153174237, 1, 0.057985050443000064, 1, 1, 1, 1, 1,
                                 0.3042733186049599, 1, 0.6648983197338092, 1, 0.03710715275750709, 1, 1, 1, 1, 1,
                                 0.0717617609858745, 1, 0.14633418247460717, 1, 1, 1, 1, 1, 1, 1, 1, 11, 1, 1, 1, 1,
                                 0.012801148666289563, 1, 0.16837008596697212, 1, 1, 1, 1, 1, 1, 1, 0.6635278656790025,
                                 1, 0.5759668092880103, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.7805673928583238, 1, 1])

        n = NeuralNet(48, 10, 50, 2, 0.1)
        resultN = n.guess(swagger_server.algorithmes.utile.centrageSolo(image, 6, 8))

        resultA = testAll(image, resultK, resultB)

        return {"kmeans": resultK, 'baye': resultB, 'neural': resultN, 'all': resultA}

    def get_3_result(self, image):
        a = self.test_data(image)
        a.pop('all', None)
        return a


benchmark = Benchmark()