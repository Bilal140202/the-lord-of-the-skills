---
description: Manage Trello boards, lists, and cards via the API.
---

# /trello

Manages Trello boards and cards.

## Prerequisites

TRELLO_API_KEY and TRELLO_TOKEN must be set as environment variables.

## Commands

### Read
/trello status       - Active boards summary.
/trello boards       - List all boards with IDs and URLs.
/trello lists <boardId>  - All lists in a board.
/trello cards <listId>   - All cards in a list with labels and due dates.

### Write
/trello create card <listId> "title" "description"
/trello create board "name" "description"
/trello move <cardId> <targetListId>

### Search
/trello search "query"   - Global search across boards and cards.
/trello sync             - Cross-reference local task.md with a board and propose updates.
