# -*- coding: utf-8 -*-
import unittest

import requests_mock

from AutoApiClient import Client, Resource
from AutoApiClient.exceptions import ResourceException


@requests_mock.Mocker()
class TestResource(unittest.TestCase):

    def setUp(self):
        super(TestResource, self).setUp()
        self.url = 'http://localhost:8686'
        self.email = 'user@email.com'
        self.fixture = {
            'id_1': {'id': 'id_1', 'key': 'foo', 'key_1': 'bar'},
            'id_2': {'id': 'id_2', 'key': 'bar', 'key_2': 'foo'}
        }

        self.client = Client(self.url)
        with requests_mock.mock() as mock:
            mock.post('%s/login' % self.url, status_code=200)
            self.client.api.login(email=self.email, password='pass')

    def test_resource(self, mock):
        mock.get('%s/api/collection/id_1' % self.url, status_code=200, json=self.fixture['id_1'])
        self.assertIsInstance(self.client.api.collection.id_1, Resource)
        self.assertIsInstance(self.client.api.collection['id_1'], Resource)

    def test_resource_not_found(self, mock):
        mock.get('%s/api/collection/id_1' % self.url, status_code=404)
        collection = self.client.api.collection
        with self.assertRaises(ResourceException):
            collection.id_1

    def test_resource_attributes(self, mock):
        mock.get('%s/api/collection/id_1' % self.url, status_code=200, json=self.fixture['id_1'])
        resource = self.client.api.collection.id_1
        for key in self.fixture['id_1']:
            self.assertEqual(resource[key], self.fixture['id_1'][key])

    def test_delete_resource(self, mock):
        mock.get('%s/api/collection/id_1' % self.url, status_code=200, json=self.fixture['id_1'])
        mock.delete('%s/api/collection/id_1' % self.url, status_code=204)
        self.assertTrue(self.client.api.collection.id_1.delete())

    def test_put_resource(self, mock):
        mock.get('%s/api/collection/id_1' % self.url, status_code=200, json=self.fixture['id_1'])
        mock.put('%s/api/collection/id_1' % self.url, status_code=204)
        resource = self.client.api.collection.id_1
        self.assertTrue(resource.put(json=self.fixture['id_2']))
        self.assertEqual(resource.id, self.fixture['id_1']['id'])
        for key in self.fixture['id_1']:
            if key != 'id' and key not in self.fixture['id_2']:
                with self.assertRaises(AttributeError):
                    resource[key]
        for key in self.fixture['id_2']:
            if key != 'id':
                self.assertEqual(resource[key], self.fixture['id_2'][key])

    def test_patch_resource(self, mock):
        mock.get('%s/api/collection/id_1' % self.url, status_code=200, json=self.fixture['id_1'])
        mock.patch('%s/api/collection/id_1' % self.url, status_code=204)
        resource = self.client.api.collection.id_1
        changes = {'foo': 'bar', 'bar': 'foo'}
        self.assertTrue(resource.patch(json=changes))
        for key in changes:
            self.assertEqual(resource[key], changes[key])
