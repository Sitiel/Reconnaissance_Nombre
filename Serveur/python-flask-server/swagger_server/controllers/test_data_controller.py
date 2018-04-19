import connexion
import six

import connexion
from swagger_server.algorithmes.kmeans import findUsingKMeans
from swagger_server.models.data import Data  # noqa: E501
import swagger_server.algorithmes.utile


def test_data(image):  # noqa: E501
    """Add a train data in database

    Add a train data in database  # noqa: E501

    :param image: Data information
    :type image: dict | bytes

    :rtype: Solution
    """

    result = findUsingKMeans([t[0] for t in trainData], [t[1] for t in trainData], image['data'],
                             swagger_server.algorithmes.utile.distValue)

    if connexion.request.is_json:
        image = Data.from_dict(connexion.request.get_json())  # noqa: E501
    return {"kmeans": result, 'baye': -1, 'neural': -1}
