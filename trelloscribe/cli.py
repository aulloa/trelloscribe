import json

import click
import toolz

from .trelloapi import download_board, find_board, read_board
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
    if board_source == 'id':
        board_data = download_board(key, token, board)
    elif board_source == 'name':
        board_data = find_board(key, token, board)
    elif board_source == 'file':
        board_data = read_board(board)

    converted = trello_to_ast(board_data)

    if format == 'raw':
        output = json.dumps(converted, indent=2)
    elif format == 'md':
        output = ast_to_md(converted)
    elif format == 'html':
        output = toolz.pipe(converted, ast_to_md, md_to_html)

    click.echo(output)
