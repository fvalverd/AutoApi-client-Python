# -*- coding: utf-8 -*-
import mock
import unittest

from AutoApi import app
from AutoApi.auth import _admin_manager_client

from AutoApiClient import Client, Collection
from AutoApiClient.exceptions import AuthException
from tests import ClientWrapper


class TestAutoApi(unittest.TestCase):

    @classmethod
    def _clean_db(cls, app, api, collection):
        with _admin_manager_client(app) as client:
            client[api][collection].drop()

    @classmethod
    def setUpClass(cls):
        super(TestAutoApi, cls).setUpClass()
        cls._clean_db(app, 'api', 'collection')
        cls.mock = mock.patch('AutoApiClient.requests', ClientWrapper(app.test_client()))
        cls.mock.start()
        cls.dummy_url = 'http://localhost:8686'

    @classmethod
    def tearDownClass(cls):
        cls.mock.stop()
        super(TestAutoApi, cls).tearDownClass()

    def test_login_and_logout(self):
        client = Client(self.dummy_url)
        with self.assertRaises(AuthException):
            client.api.collection
        self.assertTrue(client.api.login(email='admin', password='pass'))
        self.assertIsInstance(client.api.collection, Collection)
        client.api.logout()
        with self.assertRaises(AuthException):
            client.api.collection

    def test_empty_collection(self):
        client = Client(self.dummy_url)
        client.api.login(email='admin', password='pass')
        result = client.api.collection.get()
        client.api.logout()
        self.assertItemsEqual(result, [])

    def test_post(self):
        client = Client(self.dummy_url)
        client.api.login(email='admin', password='pass')
        element = client.api.collection.post(json={'key': 'value'})
        result = client.api.collection.get()
        client.api.logout()
        self.assertItemsEqual(result, [element])
