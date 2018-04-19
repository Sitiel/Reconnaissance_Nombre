import connexion
import six

from swagger_server.models.data import Data  # noqa: E501
from swagger_server.models.solution import Solution  # noqa: E501
from swagger_server import util


def test_data(image):  # noqa: E501
    """Add a train data in database

    Add a train data in database  # noqa: E501

    :param image: Data information
    :type image: dict | bytes

    :rtype: Solution
    """
    if connexion.request.is_json:
        image = Data.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
