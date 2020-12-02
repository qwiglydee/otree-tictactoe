# Sample OTree TicTacToe game

This is sample OTree-based game using live pages and multiplayer

The game implements simple Tic-Tac-Toe game. It can be run aither with 2 participants as players, or with 1 player vs AI Agent.
The AI Agent is implemented in dumb and smart versions, configurable in session.

## The code

Core Game logic is implemented in `game.py`, independently from otree stuff.

Game state is stored in model `GameSession` associated with `Subsession`. This is temporary data and should be autoremoved somehow.

Gameplay, parametrization and updating metrics is implemented on `Subsession` level.

Communication protocol is implemented on `Player` level.

The AI is impemented as either random agent, or simple minimax search algo .

Frontend part is implemented inside `Game` page. It's primitive MVC on bootstrap/jquery.
To play against AI the page sends message `ai` handled by `Player` and `Subsession` logic.

Tests are to be run with `pytest`. But they cannot use any django/otree stuff, because of weird otree initialization. So, they only test core game logic and AI.


## Deployment

The app can be run locally in container, deployed at standalone server, on Heroku from git, on Heroku from docker, or via OTreeHub.

See [DEPLOY.md](DEPLOY.md)
