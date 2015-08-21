# -*- coding: utf-8 -*-
import json


KEYS_TO_FIX = {
    'json': 'data',
    'params': 'query_string'
}


def _fix_kwargs(attribute):
    def _http_verb(*args, **kwargs):
        for old_key, new_key in KEYS_TO_FIX.iteritems():
            if old_key in kwargs:
                kwargs[new_key] = kwargs.pop(old_key)
        response = attribute(*args, **kwargs)
        response.json = lambda: json.loads(response.data)
        return response
    return _http_verb


class ClientWrapper(object):

    def __init__(self, client):
        self.client = client

    def __getattr__(self, name):
        attribute = getattr(self.client, name)
        if callable(attribute):
            return _fix_kwargs(attribute)
        return attribute

    def __getitem__(self, name):
        return getattr(self, name)
