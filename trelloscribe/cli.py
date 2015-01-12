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
    """Hi, I'm TrelloScribe. I take Trello boards and turn them into documents!"""
    # Compose a sequence of functions based on the options chosen
    # Note toolz.compose() works right to left
    read_phase = {
        'id': download_board(key, token),
        'name': toolz.compose(download_board(key, token), search_boards(key, token)),
        'file': read_board
    }
    convert_phase = {
        'raw': partial(json.dumps, indent=2),
        'md': ast_to_md,
        'html': toolz.compose(md_to_html, ast_to_md)
    }
    toolz.pipe(board, read_phase[board_source], trello_to_ast,
               convert_phase[to], partial(click.echo, file=output))
