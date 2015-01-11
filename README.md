# TrelloScribe

## Introduction

### What

Use a Trello board to compose a document or collection of documents.

### How

Each card is treated as a separate component of the overall document,
with lists (and the ordering of the cards) treated as the document
structure. The contents of the cards are concatenated and processed into
a unified document.

Trello permits Markdown syntax inside the card descriptions, which makes
this even easier -- you can preview each component while it's still in
Trello.

### Why

Motivations behind this project:

-   Collaborating over documents is a common, yet still difficult, task,
    and Trello is a terrific and easy to use medium for collaboration.
-   The card/list system provides a constant visual outline of the
    entire project.
-   Component pieces can be moved around or reorganized by drag and
    drop.
-   Different component pieces can be assigned to different people &
    commented on independent of each other -- essentially building the
    project in the same location used to manage it.

The goal is not to simulate a fully-featured word processor or similar
tool, but to highlight the usefulness of Trello's collaborative
functionality & visual interface to fit common use cases.

## Installation

### With PyPI

Not yet available

### With Github

git clone https://github.com/mcktrtl/trelloscribe.git
    pip install ./trelloscribe/

You can also use `python ./trelloscribe/setup.py`

### Pandoc

TrelloScribe requires [pandoc](http://johnmacfarlane.net/pandoc/), which
must be installed separately and included in your PATH. Installation
files for pandoc are here:

https://github.com/jgm/pandoc/releases

Note that this also means you can pipe the output from TrelloScribe into
pandoc, enabling you to export to a myraid of document formats.

## Usage

### Example

trelloscribe -b name -t md TrelloScribe

This will search all boards belonging to the owner of the API key for a
board called "TrelloScribe", and convert it to Markdown.

    trelloscribe -b file -t html ./boardexport.json

This will load an exported board from `boardexport.json` and convert it
to HTML.

### Help

View the CLI help by typing:

    $ trelloscribe --help

    Usage: trelloscribe-script.py [OPTIONS] BOARD

    Options:
      -b, --board-source [id|name|file]
                                      Choosing name will search
      --key TEXT                      Trello API Key
      --token TEXT                    Trello API Token
      -t, --to [md|html|raw]          Output format
      --help                          Show this message and exit.

### Parameters

#### -b/--board-source

Board source is an option telling TrelloScribe how to treat the board
argument.

-   `id` refers to a Trello board ID or shortlink. If a board source is
    not specified, this is default.
-   `name` refers to a Trello board name. It will search all boards
    belonging to the owner of the API key for an exact match. If it
    doesn't find one, it will exit.
-   `file` refers to a path to a JSON export of a Trello board.

#### --key & --token

These are Trello API credentials. TrelloScribe will also pull from
environmental variables `TRELLO_KEY` and `TRELLO_TOKEN`, respectively.

TrelloScribe doesn't (at least yet) help at all in this process. You can
easily enough obtain your own API credentials from Trello directly:

https://trello.com/1/appKey/generate

#### -t / --to

-   `md` will output your document in a single Markdown file. If nothing
    is specified, this is the default.
-   `html` will output your document in HTML. Currently, this will only
    generate "body" HTML (i.e. not a fully standalone HTML page).
-   `raw` will output your document in JSON, in a simple schema native
    to TrelloScribe. It is **not** the same as Trello's exported JSON.

#### board

Depending on the flag used for `--board-source`, this will either be the
board ID/shortlink, the name of the board, or the path to the exported
board.

### Advanced

#### Hiding Content

TrelloScribe will ignore any list or card that starts with a `.`
(period). You can use this for meta cards, project management, etc.

Of course, TrelloScribe will also ignore any cards which are archived
(closed).

#### Header normalization

Currently, TrelloScribe uses the following criteria to determine
document structure:

-   The name of the board is at the top of the document in H1
-   The list name is in H2
-   The card names are in H3
-   Headers inside the card description are padded +3. This means H1
    inside a card is H4 in the eventual document

More flexibility around this is planned for the future.