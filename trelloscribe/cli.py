from functools import partial
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
    pipeline = []
    if board_source == 'id':
        pipeline.append(partial(download_board, key, token))
    elif board_source == 'name':
        pipeline.extend([partial(search_boards, key, token),
                        partial(download_board, key, token)])
    elif board_source == 'file':
        pipeline.append(read_board)
    
    pipeline.append(trello_to_ast)

    if format == 'raw':
        pipeline.append(json.dumps)
    elif format == 'md':
        pipeline.append(ast_to_md)
    elif format == 'html':
        pipeline.extend([ast_to_md, md_to_html])
    pipeline.append(click.echo)
    toolz.pipe(board, *pipeline)
