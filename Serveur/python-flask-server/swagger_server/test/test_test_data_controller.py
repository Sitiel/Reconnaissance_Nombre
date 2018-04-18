# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.data import Data  # noqa: E501
from swagger_server.models.solution import Solution  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTestDataController(BaseTestCase):
    """TestDataController integration test stubs"""

    def test_test_data_master_test_data_test_data(self):
        """Test case for test_data_master_test_data_test_data

        Add a train data in database
        """
        image = Data()
        response = self.client.open(
            '//test',
            method='POST',
            data=json.dumps(image),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
