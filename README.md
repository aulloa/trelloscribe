# Trello Scribe

## What

Use a Trello board to compose a document (or collection of docs).

## How

Trello utilizes markdown in the description of cards. Each card can be treated as a separate component of the overall document, and the contents of the cards concatenated and processed into a single document.

## Why

- Collaborating over documents is a common, yet still difficult, task.
- Trello is a terrific and easy to use medium for collaboration.
- Building a project in the same location used to manage it is convenient.
- The card/list system provides a constant visual outline of the entire project.
- Component pieces can be moved around or reorganized by simple drag and drop
- Different component pieces can be assigned to different people & commented on independent of each other.

## Goals

- Pull data from Trello using a board_id or shortlink
- Pull data from Trello using a board name
- Accept a Trello exported JSON file
- Be able to pipe data out to Pandoc
- Process the board/list/card titles as content
