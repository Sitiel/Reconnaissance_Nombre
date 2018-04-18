# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.data_train import DataTrain  # noqa: E501
from swagger_server.test import BaseTestCase


class TestManageTrainingController(BaseTestCase):
    """ManageTrainingController integration test stubs"""

    def test_add_data_master_add_data_add_data(self):
        """Test case for add_data_master_add_data_add_data

        Add a train data in database
        """
        dataTrain = DataTrain()
        response = self.client.open(
            '//add',
            method='POST',
            data=json.dumps(dataTrain),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_start_train_master_start_train_start_train(self):
        """Test case for start_train_master_start_train_start_train

        Get Confusion Matrix of all Algorithms
        """
        response = self.client.open(
            '//startTrain',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
