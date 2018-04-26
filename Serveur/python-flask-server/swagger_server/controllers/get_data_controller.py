import connexion
import six

from swagger_server.models.matrix import Matrix  # noqa: E501
from swagger_server import util
from swagger_server.database import db


def get_maxtrix():  # noqa: E501
    """Get Confusion Matrix of all Algorithms

    Get Confusion Matrix of all Algorithms  # noqa: E501


    :rtype: Matrix
    """
    return {
        "data": [
        {
            "method": "baye",
            "matrix": db.getMatrix("bayesienne")
        },
        {
            "method": "kmeans",
            "matrix": db.getMatrix("kmeans")
        },
        {
            "method": "neural",
            "matrix": db.getMatrix("neural")
        },
        {
            "method": "all",
            "matrix": db.getMatrix("all")
        }
    ]}
