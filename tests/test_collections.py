# -*- coding: utf-8 -*-
import unittest

import requests_mock

from AutoApiClient import Client


@requests_mock.Mocker()
class TestCollections(unittest.TestCase):

    def setUp(self):
        super(TestCollections, self).setUp()
        self.url = 'http://localhost:8686'
        self.email = 'user@email.com'
        self.client = Client(self.url)
        with requests_mock.mock() as mock:
            mock.post('%s/login' % self.url, headers={'X-Email': self.email, 'X-Token': '123'})
            self.client.api.login(email=self.email, password='pass')
        self.collection = {
            'id_1': {'id': 'id_1', 'key': 'value'},
            'id_2': {'id': 'id_2', 'key': 'value'}
        }

    def test_get(self, mock):
        expected = self.collection.values()
        mock.get('%s/api/collection' % self.url, json=expected)

        items = self.client.api.collection.get(params={'key': 'value'})
        self.assertEqual(items, expected)

    def test_post(self, mock):
        pass
