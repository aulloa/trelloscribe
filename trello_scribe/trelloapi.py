import requests
import toolz

from string import Formatter

def get_fields(text):
    fmtr = Formatter()
    return [i[1] for i in fmtr.parse(text) if i[1]]

def remove_fields(text, payload):
    used_fields = get_fields(text)
    return {k: v for k, v in payload.items() if k not in used_fields}

class TrelloAPI():
    def __init__(self, key, token, endpoint='https://api.trello.com/1/{0}'):
        self._key = key
        self._token = token
        self._endpoint = endpoint

    def _bundle_auth(self, payload):
        return toolz.merge(payload, {'key': self._key, 'token': self._token})

    def _request(self, method, path, *args, **kwargs):
        url = self._endpoint.format(path).format(**kwargs)
        payload = toolz.thread_last(kwargs, (remove_fields, path),
                                    self._bundle_auth)
        req = requests.request(method, url, data=payload)
        req.raise_for_status()
        return req.json()