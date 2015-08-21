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

    def test_insert_and_retrieve_an_element(self):
        client = Client(self.dummy_url)
        client.api.login(email='admin', password='pass')
        item = client.api.collection.post(json={'key': 'value'})

        self.assertIn('id', item)
        result = client.api.collection.get()
        self.assertItemsEqual(result, [item])
        element = client.api.collection[item['id']]
        for key, value in item.iteritems():
            self.assertEqual(element[key], value)
        client.api.logout()

    def test_update_some_data(self):
        client = Client(self.dummy_url)
        client.api.login(email='admin', password='pass')
        item = client.api.collection.post(json={'key': 'value'})

        new_fields = {'key': 'other_value', 'other_key': 'eulav'}
        element = client.api.collection[item['id']]
        element.patch(json=new_fields)
        for key, value in new_fields.iteritems():
            self.assertEqual(element[key], value)

        element = client.api.collection[item['id']]
        for key, value in new_fields.iteritems():
            self.assertEqual(element[key], value)

        client.api.logout()

    def test_replace_all_data(self):
        client = Client(self.dummy_url)
        client.api.login(email='admin', password='pass')
        old_fields = {'key': 'value'}
        item = client.api.collection.post(json=old_fields)

        new_fields = {'value': 'key'}
        element = client.api.collection[item['id']]
        element.put(json=new_fields)
        for key in old_fields:
            if key not in new_fields:
                with self.assertRaises(AttributeError):
                    element[key]
        for key, value in new_fields.iteritems():
            self.assertEqual(element[key], value)

        element = client.api.collection[item['id']]
        for key in old_fields:
            if key not in new_fields:
                with self.assertRaises(AttributeError):
                    element[key]
        for key, value in new_fields.iteritems():
            self.assertEqual(element[key], value)

        client.api.logout()
