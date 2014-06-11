# drifter.api
# Executes queries to the Phoenix-API on behalf of the Drifter service.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Jun 10 10:46:15 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: api.py [] benjamin@bengfort.com $

"""
Executes queries to the Phoenix-API on behalf of the Drifter service.
"""

##########################################################################
## Imports
##########################################################################

import json
import requests

from drifter import settings

##########################################################################
## Drifter Class
##########################################################################

class Drifter(object):

    def __init__(self, api_root=None, api_key=None):
        self.api_root = api_root or settings['api_root']
        self.api_key  = api_key or settings['api_key']

    def build_endpoint(self, *path):
        path = '/'.join(path)
        return "%s/%s" % (self.api_root, path)

    def build_headers(self, headers={}):
        default = {
            'API-Key': self.api_key
        }
        default.update(headers)
        return default

    def build_payload(self, data, headers={}):
        headers.update({'content-type': 'application/json'})
        payload = json.dumps(data)
        return headers, payload

    def execute(self, method, url, **kwargs):
        # Set arguments to pass to requests
        kwargs['headers'] = self.build_headers(kwargs.pop('headers', {}))
        kwargs['verify']  = kwargs.get('verify', False)
        kwargs['timeout'] = kwargs.get('timeout', 30)

        response = method(url, **kwargs)
        if response.status_code == requests.codes.ok:
            return response.json()
        response.raise_for_status()

    def get(self, url, **kwargs):
        return self.execute(requests.get, url, **kwargs)

    def put(self, url, data, **kwargs):
        headers, payload  = self.build_payload(data)
        kwargs['headers'] = headers
        kwargs['data']    = payload
        return self.execute(requests.put, url, **kwargs)

    def post(self, url, data, **kwargs):
        headers, payload  = self.build_payload(data)
        kwargs['headers'] = headers
        kwargs['data']    = payload
        return self.execute(requests.post, url, **kwargs)

    def delete(self, url, **kwargs):
        return self.execute(requests.delete, url, **kwargs)

if __name__ == '__main__':
    drifter  = Drifter()
    print drifter.api_key
    endpoint = drifter.build_endpoint('users', 'me')
    print endpoint
    print json.dumps(drifter.get(endpoint), indent=4)
