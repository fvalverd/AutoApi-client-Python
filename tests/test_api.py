# -*- coding: utf-8 -*-
import unittest

import requests_mock

from AutoApiClient import Api, Client


class TestApi(unittest.TestCase):

    def setUp(self):
        super(TestApi, self).setUp()
        self.url = 'http://localhost:8686'
        self.client = Client(self.url)

    def test_api(self):
        self.assertIsInstance(self.client.api, Api)
        self.assertIsInstance(self.client['api'], Api)

    @requests_mock.mock()
    def test_login_status(self, mock):
        mock.post('%s/login' % self.url, status_code=200)
        self.client.api.login(email='user@email.com', password='pass')
        self.assertTrue(self.client.api.logged)

    @requests_mock.mock()
    def test_login_headers(self, mock):
        headers = {'X-Email': 'user@email.com', 'X-Token': 'Token123'}
        mock.post('%s/login' % self.url, status_code=200, headers=headers)
        self.client.api.login(email='user@email.com', password='pass')
        self.assertEqual(self.client.api.headers, headers)

    @requests_mock.mock()
    def test_login_failed(self, mock):
        mock.post('%s/login' % self.url, status_code=400)
        self.client.api.login(email='user@email.com', password='pass')
        self.assertFalse(self.client.api.logged)
        self.assertEqual(self.client.api.headers, {})

    @requests_mock.mock()
    def test_logout_status(self, mock):
        mock.post('%s/logout' % self.url, status_code=204)
        self.client.api.logout()
        self.assertFalse(self.client.api.logged)

    @requests_mock.mock()
    def test_logout_headers(self, mock):
        mock.post('%s/logout' % self.url, status_code=204)
        self.client.api.logout()
        self.assertEqual(self.client.api.headers, {})

    @requests_mock.mock()
    def test_login_failed(self, mock):
        mock.post('%s/logout' % self.url, status_code=401)
        self.client.api.logout()
        self.assertFalse(self.client.api.logged)
        self.assertEqual(self.client.api.headers, {})
