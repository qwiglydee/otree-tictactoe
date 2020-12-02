# Sample OTree TicTacToe game

This is sample OTree-based game using live pages and multiplayer.

The game implements classic 3x3 Tic-Tac-Toe game in timed mode. It is played either between 2 participants, or 1 participant vs AI agent.
It consists of 3 pages: Into, Game, Results. All the gameplay happens in the Game page.

## Gameplay

- player opens Intro pages with brief game description
- player proceeds to the game page:
  - an indicator of symbol the player uses
  - a game board
  - an indicator of current turn
  - a message 'Make your move' or 'Wait for your opponent'
  - a timer indicating remaining time
- player clicks a cell in the board to place their symbol
- in case of error, a popup appears with message 'Not your turn' or 'Invalid move'
- otherwise, the symbol is placed on the board
- page waits for other player or AI agent to make their move
- once other player makes move, the board refreshes with new symbols
- the cycle repeats on the game page until one of the players wins or time expires
- a message appears "You won!", "You lost!", "Tie!" or "Timeout expired"
- the winning pattern is highlighted in green for winner and in red for loser
- the usual button 'next' appears at bottom of the page
- player proceeds to Results page with indication 'You have made N moves and won/lost in M seconds.' or 'The game drawn in N moves and M seconds', or 'The game timeout expired.'

## Session parameters

- `duration_min`, `duration_max` -- duration of a round, in seconds. Value is choosen randomly in given range.
- `P1_symbol` = `x`/`o` -- a symbol for P1 player, empty to select randomly
- `ai_class` = `dumb`/`smart` -- an algorithm for AI agent P2 player, empty for 2-participant sessions

## Metrics

For each round:
- `duration` (seconds) -- the configured or randomly chosen duration of the round
- `ai_class` -- class of ai agent used, or null
- `completed` -- indicates if the game was completed or timeout expired
- `moves` -- total moves done in the round

For each player:
- `moves` -- number of moves done
- `win` -- indicator of the round outcome for each player

# The code

Core Game logic is implemented in `game.py`, independently from otree stuff.

Game state is stored in model `GameSession` associated with `Subsession`. This is temporary data and should be autoremoved somehow.

Gameplay, parametrization and updating metrics is implemented on `Subsession` level.

Communication protocol is implemented on `Player` level.

The AI is impemented as either random agent, or simple minimax search algo .

Frontend part is implemented inside `Game` page. It's primitive MVC on bootstrap/jquery.
To play against AI the page sends message `ai` handled by `Player` and `Subsession` logic.

Tests are to be run with `pytest`. But they cannot use any django/otree stuff, because of weird otree initialization. So, they only test core game logic and AI.


# Deployment

The app can be run locally in container, deployed at standalone server, on Heroku from git, on Heroku from docker, or via OTreeHub.

See [DEPLOY.md](DEPLOY.md)
