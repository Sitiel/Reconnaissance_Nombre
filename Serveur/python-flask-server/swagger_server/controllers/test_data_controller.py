import connexion
from swagger_server.algorithmes.kmeans import findUsingKMeans
from swagger_server.controllers.manage_training_controller import trainData
from swagger_server.models.data import Data  # noqa: E501
import swagger_server.algorithmes.utile


def test_data_master_test_data_test_data(image):  # noqa: E501
    """Add a train data in database

    Add a train data in database  # noqa: E501

    :param image: Data information
    :type image: dict | bytes

    :rtype: Solution
    """
    result = findUsingKMeans([t[0] for t in trainData], image, swagger_server.algorithmes.utile.distValue)
    print(result)

    if connexion.request.is_json:
        image = Data.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
    