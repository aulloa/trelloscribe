import json
import webbrowser

import requests


def to_gist(content, board_name):
    filename = '{0}.md'.format(board_name.lower().replace(' ', '-'))
    description = 'TrelloScribe export of {0}'.format(board_name)
    return webbrowser.open(send_gist(content, file_name, description))

def send_gist(content, filename, description, public=False):
    payload = {
        'public': public,
        'description': description,
        'files': {
            filename: {'content': content}
        }
    }
    req = requests.post('https://api.github.com/gists',
                        headers={'Accept': 'application/vnd.github.v3+json'},
                        data=json.dumps(payload))
    return req.json()['html_url']
