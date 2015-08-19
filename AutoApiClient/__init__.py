# -*- coding: utf-8 -*-
import requests

from AutoApiClient.exceptions import AutoApiAuthException, AutoApiResourceException


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


class AutoApiHttp(object):

    def url(self):
        return "%s/%s" % (self.parent.url(), self.id)

    def _headers(self):
        return self.parent._headers()

    def _http(self, fun, url=None, *a, **ka):
        return fun(url or self.url(), headers=self._headers(), *a, **ka)


class Api(AutoApiHttp):

    def __init__(self, parent, api_name):
        self.parent = parent
        self.id = api_name
        self.logged = False
        self.headers = {}

    def url(self):
        return "%s/%s" % (self.parent.url, self.id)

    def _headers(self):
        return self.headers

    def login(self, email, password):
        response = self._http(
            requests.post,
            url="%s/login" % self.parent.url,
            params={'api': self.id, 'email': email, 'password': password}
        )
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
        self._http(
            requests.post,
            url="%s/logout" % self.parent.url,
            json={'api': self.id}
        )
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


class Collection(AutoApiHttp):

    def __init__(self, parent, collection_name):
        self.parent = parent
        self.id = collection_name

    def get(self, params=None):
        response = self._http(requests.get, params=params)
        if response.status_code == 200:
            return response.json()

    def post(self, json):
        response = self._http(requests.post, json=json)
        if response.status_code == 201:
            return response.json()

    def __getattribute__(self, resource_id):
        try:
            return object.__getattribute__(self, resource_id)
        except AttributeError:
            return Resource(self, resource_id)

    def __getitem__(self, resource_id):
        return self.__getattribute__(resource_id)


class Resource(AutoApiHttp):

    def __init__(self, parent, resource_id):
        self.parent = parent
        self.id = resource_id
        response = self._http(requests.get)
        if response.status_code == 200:
            for key, value in response.json().iteritems():
                object.__setattr__(self, key, value)
        else:
            raise AutoApiResourceException("Not found resource")

    def delete(self):
        response = self._http(requests.delete)
        return response.status_code == 204

    def put(self, json):
        response = self._http(requests.put, json=json)
        return response.status_code == 204

    def patch(self, json):
        response = self._http(requests.patch, json=json)
        return response.status_code == 204
