import connexion
import six

import connexion
from swagger_server.algorithmes.kmeans import findUsingKMeans
from swagger_server.algorithmes.bayesienne import findUsingBaye,trainBaye
from swagger_server.algorithmes.neural import NeuralNet
from swagger_server.benchmark import benchmark
from swagger_server.models.data import Data  # noqa: E501
import swagger_server.algorithmes.utile
from swagger_server.database import db
import random


def test_data(image):  # noqa: E501
    """Test a data

    Test a data and return the output  # noqa: E501

    :param image: Data information
    :type image: dict | bytes

    :rtype: Solution
    """

    return benchmark.test_data(image['data'])
