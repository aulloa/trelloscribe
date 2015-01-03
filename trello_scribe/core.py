import argparse
import os

import toolz

from .trelloapi import TrelloAPI

def download_board(trello_key, trello_token, board):
    trello = TrelloAPI(trello_key, trello_token)
    return trello._request('get', 'boards/{board}', board=board, cards='open',
                           lists='open')

def concatenate_cards(board_data):
    return '\n\n'.join(c['desc'].strip() for c in board_data['cards'])

def main():
    parser = argparse.ArgumentParser(description='Trello Scribe')
    parser.add_argument('board', action='store',
                        help='Trello board to fetch (id or shortlink)')
    parser.add_argument('--trello-key', action='store',
                        default=os.getenv('trello_key'), help='Trello API Key')
    parser.add_argument('--trello-token', action='store',
                        default=os.getenv('trello_token'), help='Trello API Token')
    args = parser.parse_args()

    board_data = download_board(args.trello_key, args.trello_token, args.board)
    toolz.pipe(board_data, concatenate_cards, print)
