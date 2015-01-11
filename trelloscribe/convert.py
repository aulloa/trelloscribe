import pypandoc
import toolz


def trello_to_ast(board):
    new_board = {
        'name': board.get('name')
    }
    hidden_lists = {li['id'] for li in board['lists']
                             if li['closed'] or
                                li['name'].startswith('.')}
    new_board['lists'] = []
    for li in filter(lambda x: x['id'] not in hidden_lists, board['lists']):
        name = li['name']
        cards = [{'name': c['name'], 'desc': c['desc']}
                 for c in board['cards']
                 if c['idList'] == li['id'] and not c['closed']]
        new_board['lists'].append({'name': name, 'cards': cards})
    return new_board


def astcard_to_md(card):
    if card['desc']:
        fstring = '### {0}\n\n{1}'
        contents = pypandoc.convert(card['desc'], 'markdown', format='markdown',
                                    extra_args=['--atx-headers',
                                                '--base-header-level=4'])
    else:
        fstring = '### {0}{1}'
        contents = ''
    return fstring.format(card['name'], contents.strip())

def astlist_to_md(list_):
    concated_cards = '\n\n'.join(map(astcard_to_md, list_['cards']))
    return '## {0}\n\n{1}'.format(list_['name'], concated_cards)

def ast_to_md(board):
    markdowned = '\n\n'.join(map(astlist_to_md, board['lists']))
    return '# {0}\n\n{1}'.format(board['name'], markdowned)

def md_to_html(md):
    return pypandoc.convert(md, 'html', format='markdown')
