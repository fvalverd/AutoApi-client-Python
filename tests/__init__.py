# -*- coding: utf-8 -*-
import json


class ClientWrapper(object):

    def __init__(self, client):
        self.client = client

    def fix_kwargs(self, attribute):
        def http_verb(url, *args, **kwargs):
            for old_key, new_key in {'json': 'data', 'params': 'query_string'}.iteritems():
                if old_key in kwargs:
                    kwargs[new_key] = kwargs[old_key]
                    del kwargs[old_key]
            response = attribute(url, *args, **kwargs)
            response.json = lambda: json.loads(response.data)
            return response
        return http_verb

    def __getattr__(self, name):
        return self.fix_kwargs(getattr(self.client, name))

    def __getitem__(self, name):
        return getattr(self, name)
