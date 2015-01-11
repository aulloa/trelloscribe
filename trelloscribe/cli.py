from functools import partial
from itertools import chain
import json

import click
import toolz

from .trelloapi import download_board, search_boards, read_board
from .convert import trello_to_ast, ast_to_md, md_to_html


@click.command()
@click.option('-b', '--board-source', help='Choosing name will search',
              type=click.Choice(['id', 'name', 'file']))
@click.option('--key', help='Trello API Key', envvar='TRELLO_KEY')
@click.option('--token', help='Trello API Token', envvar='TRELLO_TOKEN')
@click.option('-t', '--format', type=click.Choice(['md', 'html', 'raw']),
              default='md')
@click.argument('board')
def cli(board_source, key, token, format, board):
    read_phase = {
        'id': [partial(download_board, key, token), trello_to_ast],
        'name': [partial(search_boards, key, token), 
                 partial(download_board, key, token),  trello_to_ast],
        'file': [read_board,  trello_to_ast]
    }
    convert_phase = {
        'raw': [json.dumps, click.echo],
        'md': [ast_to_md, click.echo],
        'html': [ast_to_md, md_to_html, click.echo]
    }
    toolz.pipe(board, *chain(read_phase[board_source], convert_phase[format]))
