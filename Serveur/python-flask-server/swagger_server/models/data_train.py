# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.data import Data  # noqa: F401,E501
from swagger_server.models.solution import Solution  # noqa: F401,E501
from swagger_server import util


class DataTrain(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, data: Data=None, solution: Solution=None):  # noqa: E501
        """DataTrain - a model defined in Swagger

        :param data: The data of this DataTrain.  # noqa: E501
        :type data: Data
        :param solution: The solution of this DataTrain.  # noqa: E501
        :type solution: Solution
        """
        self.swagger_types = {
            'data': Data,
            'solution': Solution
        }

        self.attribute_map = {
            'data': 'data',
            'solution': 'solution'
        }

        self._data = data
        self._solution = solution

    @classmethod
    def from_dict(cls, dikt) -> 'DataTrain':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The dataTrain of this DataTrain.  # noqa: E501
        :rtype: DataTrain
        """
        return util.deserialize_model(dikt, cls)

    @property
    def data(self) -> Data:
        """Gets the data of this DataTrain.


        :return: The data of this DataTrain.
        :rtype: Data
        """
        return self._data

    @data.setter
    def data(self, data: Data):
        """Sets the data of this DataTrain.


        :param data: The data of this DataTrain.
        :type data: Data
        """

        self._data = data

    @property
    def solution(self) -> Solution:
        """Gets the solution of this DataTrain.


        :return: The solution of this DataTrain.
        :rtype: Solution
        """
        return self._solution

    @solution.setter
    def solution(self, solution: Solution):
        """Sets the solution of this DataTrain.


        :param solution: The solution of this DataTrain.
        :type solution: Solution
        """

        self._solution = solution
