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

    def login(self, email, password):
        response = requests.post("%s/login" % self.client.url, json={
            'api': self.name,
            'email': email,
            'password': password
        })
        if response.status_code == 200:
            self.logged = True
            self.headers = {
                'X-User': response.headers['X-Email'],
                'X-Token': response.headers['X-Token']
            }
        return self.logged

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

    def __getattribute__(self, resource_id):
        if resource_id in ['get', 'post']:
            return object.__getattribute__(self, resource_id)
        return Resource(self, resource_id)

    def __getitem__(self, resource_id):
        return Resource(self, resource_id)

    def get(self, data):
        raise Exception("Implement !!!")

    def post(self, data):
        raise Exception("Implement !!!")


class Resource(object):

    def __init__(self, collection, resource_id):
        raise Exception("Implement !!!")

    def get(self):
        raise Exception("Implement !!!")

    def delete(self):
        raise Exception("Implement !!!")

    def put(self, data):
        raise Exception("Implement !!!")

    def patch(self, data):
        raise Exception("Implement !!!")
