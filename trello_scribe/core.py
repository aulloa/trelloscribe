import argparse
import json
import operator
import os

import toolz

from .trelloapi import TrelloAPI


def download_board(trello_key, trello_token, board):
    trello = TrelloAPI(trello_key, trello_token)
    return trello._request('get', 'boards/{board}', board=board, cards='open',
                           lists='open')

def search_boards(trello_key, trello_token, board_name):
    trello = TrelloAPI(trello_key, trello_token)
    all_boards = trello._request('get', 'members/me/boards', filter='open',
                           fields='name')
    try:
        return toolz.thread_last(
            all_boards,
            (filter, lambda x: x['name'] == board_name),
            toolz.first,
            (toolz.get, 'id')
        )
    except:
        return None


def process_card(card):
    if card['desc']:
        fstring = '### {0}\n\n{1}'
    else:
        fstring = '### {0}{1}'
    return fstring.format(card['name'], card['desc'].strip())


def process_list(list_, cards):
    concatenated_cards = '\n\n'.join(process_card(c)
                                     for c in cards
                                     if not c['name'].startswith('.'))
    return '## {0}\n\n{1}'.format(list_['name'], concatenated_cards)


def process_board(board_data):
    separated_cards = toolz.partitionby(operator.itemgetter('idList'),
                                        board_data['cards'])
    markdowned = '\n\n'.join(process_list(l, c)
                             for l, c in zip(board_data['lists'], separated_cards)
                             if not l['name'].startswith('.'))
    return '# {0}\n\n{1}'.format(board_data['name'], markdowned)


def parse_args():
    parser = argparse.ArgumentParser(description='Trello Scribe')
    parser.add_argument('-b', action='store', dest='board',
                        help='Trello board to fetch (id or shortlink -- for board name, use -s)')
    parser.add_argument('-s', action='store', dest='search',
                        help='Search Trello boards for a board name')
    parser.add_argument('-r', action='store', dest='read',
                        help='Read a Trello export from file (JSON)')
    parser.add_argument('--trello-key', action='store',
                        default=os.getenv('trello_key'), help='Trello API Key')
    parser.add_argument('--trello-token', action='store',
                        default=os.getenv('trello_token'), help='Trello API Token')
    return parser.parse_args()

def main():
    args = parse_args()
    if args.board:
        board_data = download_board(args.trello_key, args.trello_token, args.board)
    elif args.search:
        board_id = search_boards(args.trello_key, args.trello_token, args.search)
        board_data = download_board(args.trello_key, args.trello_token, board_id)
    elif args.read:
        with open(args.read, 'r') as f:
            board_data = json.load(f)
            board_data['cards'] = [c for c in board_data['cards']
                                   if not c['closed']]
            board_data['lists'] = [l for l in board_data['lists']
                                   if not l['closed']]

    toolz.pipe(board_data, process_board, print)
