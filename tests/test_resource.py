# -*- coding: utf-8 -*-
import unittest

import requests_mock

from AutoApiClient import Client, Resource


@requests_mock.Mocker()
class TestResource(unittest.TestCase):

    def setUp(self):
        super(TestResource, self).setUp()
        self.url = 'http://localhost:8686'
        self.email = 'user@email.com'
        self.fixture = {
            'id_1': {'id': 'id_1', 'key': 'value'},
            'id_2': {'id': 'id_2', 'key': 'value'}
        }

        self.client = Client(self.url)
        with requests_mock.mock() as mock:
            mock.post('%s/login' % self.url, status_code=200)
            self.client.api.login(email=self.email, password='pass')

    def test_resource(self, mock):
        mock.get('%s/api/collection/id_1' % self.url, status_code=200, json=self.fixture['id_1'])
        self.assertIsInstance(self.client.api.collection.id_1, Resource)
        self.assertIsInstance(self.client.api.collection['id_1'], Resource)