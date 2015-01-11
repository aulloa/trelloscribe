import argparse
import operator
import os

import toolz

from .trelloapi import download_board, find_board, read_board
from .convert import trello_to_ast, ast_to_md, md_to_html


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
    parser.add_argument('--html', action='store_true', dest='html', default=False, 
                        help='Export to HTML')
    return parser.parse_args()

def main():
    args = parse_args()
    if args.board:
        board_data = download_board(args.trello_key, args.trello_token, args.board)
    elif args.search:
        board_data = find_board(args.trello_key, args.trello_token, args.search)
    elif args.read:
        board_data = read_board(args.read)

    output = toolz.pipe(board_data, trello_to_ast, ast_to_md)
    if args.html:
        print(md_to_html(output))
    else:
        print(output)

    
