import json
from string import Formatter

import requests
import toolz

def download_board(key, token, board, *args, **kwargs):
    """Downloads the board from Trello. Accepts idBoard or shortLink"""
    method = 'get'
    path = 'boards/{board}'
    return execute_request(key, token, method, path, board=board, cards='open',
                           lists='open')


def search_boards(key, token, board_name):
    method = 'get'
    path = 'members/me/boards'
    all_boards = execute_request(key, token, method, path, filter='open',
                                 fields='name')
    try:
        return toolz.thread_last(all_boards,
                                 (filter, lambda x: x['name'] == board_name),
                                 toolz.first,
                                 (toolz.get, 'id'))
    except:
        raise ValueError('No board found with that name')


def execute_request(key, token, method, path, *args, **kwargs):
    url = 'https://api.trello.com/1/{0}'.format(path).format(**kwargs)
    payload = toolz.thread_last(kwargs,
                                (remove_used_fields, path),
                                (bundle_auth, key, token))
    req = requests.request(method, url, data=payload)
    req.raise_for_status()
    return req.json()


def read_board(fn):
    with open(fn, 'r') as f:
        board_data = json.load(f)
        board_data['cards'] = [c for c in board_data['cards']
                               if not c['closed']]
        board_data['lists'] = [l for l in board_data['lists']
                               if not l['closed']]
    return board_data

def extract_used_fields(text):
    fmtr = Formatter()
    return [i[1] for i in fmtr.parse(text) if i[1]]


def remove_used_fields(text, payload):
    used_fields = extract_used_fields(text)
    return {k: v for k, v in payload.items() if k not in used_fields}


def bundle_auth(key, token, payload):
    return toolz.merge(payload, {'key': key, 'token': token})