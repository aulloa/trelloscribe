import argparse
import operator
import os

import toolz

from .trelloapi import TrelloAPI


def download_board(trello_key, trello_token, board):
    trello = TrelloAPI(trello_key, trello_token)
    return trello._request('get', 'boards/{board}', board=board, cards='open',
                           lists='open')


def process_card(card):
    if card['desc']:
        fstring = '### {0}\n\n{1}'
    else:
        fstring = '### {0}{1}'
    return fstring.format(card['name'], card['desc'].strip())


def process_list(list_, cards):
    concatenated_cards = '\n\n'.join(process_card(c) for c in cards)
    return '## {0}\n\n{1}'.format(list_['name'], concatenated_cards)


def process_board(board_data):
    separated_cards = toolz.partitionby(operator.itemgetter('idList'),
                                        board_data['cards'])
    markdowned = '\n\n'.join(process_list(l, c)
                             for l, c in zip(board_data['lists'], separated_cards))
    return '# {0}\n\n{1}'.format(board_data['name'], markdowned)


def parse_args():
    parser = argparse.ArgumentParser(description='Trello Scribe')
    parser.add_argument('board', action='store',
                        help='Trello board to fetch (id or shortlink)')
    parser.add_argument('--trello-key', action='store',
                        default=os.getenv('trello_key'), help='Trello API Key')
    parser.add_argument('--trello-token', action='store',
                        default=os.getenv('trello_token'), help='Trello API Token')
    return parser.parse_args()

def main():
    args = parse_args()
    board_data = download_board(args.trello_key, args.trello_token, args.board)
    toolz.pipe(board_data, process_board, print)
