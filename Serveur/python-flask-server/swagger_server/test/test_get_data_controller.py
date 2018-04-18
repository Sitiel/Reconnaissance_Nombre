# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.matrix import Matrix  # noqa: E501
from swagger_server.test import BaseTestCase


class TestGetDataController(BaseTestCase):
    """GetDataController integration test stubs"""

    def test_get_maxtrix_master_get_maxtrix_get_maxtrix(self):
        """Test case for get_maxtrix_master_get_maxtrix_get_maxtrix

        Get Confusion Matrix of all Algorithms
        """
        response = self.client.open(
            '//getMatrix',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
