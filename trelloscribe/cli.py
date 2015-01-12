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
@click.option('-t', '--to', type=click.Choice(['md', 'html', 'raw']),
              default='md', help='Output format')
@click.option('-o', '--output', help='Output file name', type=click.File(mode='wb', lazy=True))
@click.argument('board')
def cli(board_source, key, token, to, output, board):
    read_phase = {
        'id': [download_board(key, token), trello_to_ast],
        'name': [search_boards(key, token), download_board(key, token),
                 trello_to_ast],
        'file': [read_board,  trello_to_ast]
    }
    convert_phase = {
        'raw': [json.dumps],
        'md': [ast_to_md],
        'html': [ast_to_md, md_to_html]
    }
    write_phase = lambda o: [lambda x: click.echo(x, file=o)]
    toolz.pipe(board, *chain(read_phase[board_source], convert_phase[to], write_phase(output)))
