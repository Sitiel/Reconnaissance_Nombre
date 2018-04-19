import connexion
import six

from swagger_server.models.data_train import DataTrain  # noqa: E501


trainData = []


def add_data_master_add_data_add_data(dataTrain):  # noqa: E501
    """Add a train data in database

    Add a train data in database  # noqa: E501

    :param dataTrain: Data information
    :type dataTrain: dict | bytes

    :rtype: None
    """
    trainData.append([dataTrain['data'], dataTrain['solution']])
    print(trainData)
    if connexion.request.is_json:
        dataTrain = DataTrain.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def start_train_master_start_train_start_train():  # noqa: E501
    """Get Confusion Matrix of all Algorithms

    Get Confusion Matrix of all Algorithms  # noqa: E501


    :rtype: None
    """
    return 'do some magic!'
