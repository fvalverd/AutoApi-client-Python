# -*- coding: utf-8 -*-
import unittest

import requests_mock

from AutoApiClient import Client, Collection
from AutoApiClient.exceptions import AutoApiAuthException


class TestCollectionNotLogged(unittest.TestCase):

    def setUp(self):
        super(TestCollectionNotLogged, self).setUp()
        self.url = 'http://localhost:8686'
        self.client = Client(self.url)

    def test_collection_auth_exception(self):
        with self.assertRaises(AutoApiAuthException):
            self.client.api.collection
        with self.assertRaises(AutoApiAuthException):
            self.client.api['collection']


@requests_mock.Mocker()
class TestCollection(unittest.TestCase):

    def setUp(self):
        super(TestCollection, self).setUp()
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

    def test_collection(self, mock):
        self.assertIsInstance(self.client.api.collection, Collection)

    def test_get(self, mock):
        mock.get('%s/api/collection' % self.url, status_code=200, json=self.fixture.values())
        items = self.client.api.collection.get(params={'key': 'value'})
        self.assertEqual(items, self.fixture.values())

    def test_post(self, mock):
        mock.post('%s/api/collection' % self.url, status_code=201, json=self.fixture['id_1'])
        item = self.client.api.collection.post(json=self.fixture['id_1'])
        self.assertEqual(item, self.fixture['id_1'])
