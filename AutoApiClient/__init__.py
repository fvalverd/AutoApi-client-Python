# -*- coding: utf-8 -*-
import requests

from AutoApiClient.exceptions import AutoApiAuthException


class Client(object):

    def __init__(self, url):
        self.url = url

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except Exception:
            object.__setattr__(self, name, Api(self, name))
        finally:
            return object.__getattribute__(self, name)

    def __getitem__(self, name):
        return self.__getattribute__(name)


class Api(object):

    def __init__(self, client, name):
        self.client = client
        self.name = name
        self.logged = False
        self.headers = {}

    def login(self, email, password):
        response = requests.post("%s/login" % self.client.url, json={
            'api': self.name,
            'email': email,
            'password': password
        })
        if response.status_code == 200:
            self.logged = True
            self.headers = {
                'X-Email': response.headers.get('X-Email'),
                'X-Token': response.headers.get('X-Token')
            }
        else:
            self.logged = False
            self.headers = {}
        return self.logged

    def logout(self):
        response = requests.post("%s/logout" % self.client.url, json={
            'api': self.name
        })
        self.logged = False
        self.headers = {}

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            if not object.__getattribute__(self, 'logged'):
                raise AutoApiAuthException(
                    "You must be logged, use login method"
                )
            object.__setattr__(self, name, Collection(self, name))
            return object.__getattribute__(self, name)

    def __getitem__(self, name):
        return self.__getattribute__(name)


class Collection(object):

    def __init__(self, api, name):
        self.api = api
        self.name = name

    def get(self, params=None):
        response = requests.get(
            "%s/%s/%s" % (
                object.__getattribute__(self, 'api').client.url,
                object.__getattribute__(self, 'api').name,
                object.__getattribute__(self, 'name')
            ),
            params=params,
            headers=object.__getattribute__(self, 'api').headers
        )
        if response.status_code == 200:
            return response.json()

    def post(self, json):
        response = requests.post(
            "%s/%s/%s" % (
                object.__getattribute__(self, 'api').client.url,
                object.__getattribute__(self, 'api').name,
                object.__getattribute__(self, 'name')
            ),
            json=json,
            headers=object.__getattribute__(self, 'api').headers
        )
        if response.status_code == 201:
            return response.json()

    def __getattribute__(self, resource_id):
        try:
            return object.__getattribute__(self, resource_id)
        except AttributeError:
            return Resource(self, resource_id)

    def __getitem__(self, resource_id):
        return self.__getattribute__(resource_id)


class Resource(object):

    def __init__(self, collection, resource_id):
        self.collection = collection
        self.resource_id = resource_id
        response = requests.get(
            "%s/%s/%s/%s" % (
                object.__getattribute__(self, 'collection').api.client.url,
                object.__getattribute__(self, 'collection').api.name,
                object.__getattribute__(self, 'collection').name,
                object.__getattribute__(self, 'resource_id')
            ),
            headers=object.__getattribute__(self, 'collection').api.headers
        )
        if response.status_code == 200:
            for key, value in response.json().iteritems():
                object.__setattr__(self, key, value)
        else:
            raise Exception("Not found resource")

    def delete(self):
        raise Exception("Not Implement !!!")

    def put(self, data):
        raise Exception("Not Implement !!!")

    def patch(self, data):
        raise Exception("Not Implement !!!")
