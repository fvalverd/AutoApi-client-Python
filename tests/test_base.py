# -*- coding: utf-8 -*-
import unittest

import requests_mock

from AutoApiClient import Api, Client, Collection
from AutoApiClient.exceptions import AutoApiAuthException


class TestBase(unittest.TestCase):

    def setUp(self):
        super(TestBase, self).setUp()
        self.url = 'http://localhost:8686'
        self.email = 'user@email.com'
        self.client = Client(self.url)

    def test_api_instance(self):
        self.assertIsInstance(self.client.api, Api)

    def test_api_instance_as_item(self):
        self.assertIsInstance(self.client['api'], Api)

    def test_collection_auth_exception(self):
        with self.assertRaises(AutoApiAuthException):
            self.client.api.collection

    def test_collection_auth_exception_as_item(self):
        with self.assertRaises(AutoApiAuthException):
            self.client.api['collection']

    @requests_mock.mock()
    def test_collection_instance(self, mock):
        mock.post('%s/login' % self.url, headers={'X-Email': self.email, 'X-Token': '123'})
        self.client.api.login(email=self.email, password='pass')
        self.assertIsInstance(self.client.api.collection, Collection)
