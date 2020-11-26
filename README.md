# Otree TicTacToe game

This is sample Otree-backed game exploiting live pages, multiplayer, and AI-player.

The game implements simple Tic-Tac-Toe game. It can be run aither with 2 participants as players, or with 1 player vs AI Agent.
The AI Agent is implemented in dumb and smart versions, configurable in session.

The application is dockerized for local development and deployment.


## Local development

### Basic

- copy `deploy.env` into `.env` and tweak parameters. in particular, variables `USERUID` and `USERGID` should match local developer user, for sources mount to work.
- build install and run everything with `docker-compose -f docker-compose.devel.yaml up -d`
- local source directory is mounted into it
- container will not start anything, but instead to wait for commands
- invoke `docker-composer -f docker-compose.devel.yaml exec web otree devserver` to start the devserver

### VSCode

Install 'Remote Container' extension.
It will see file `.devcontainer.json` and provide option 'Reopen in container' and build everything automatically and edit files inside container.
Use `(Ctrl|Shift)-F5` to start/restart/debug devserver.

### Testing

Unit tests for game logic and ai are in `tictactoe/tests` directory. They are to be run with `pytest`.
VSCode is configured to run tests from UI.

## Deployment

### Local/standalone server

- copy `deploy.env` into `.env` and tweak parameters
- build install and start everything: `docker-compose up -d`

Initializing database:
- `docker-compose exec web otree resetdb` -- to initialize database

### Heroku

- create an app on Heroku
- attach redis and postgres services (this should also create config vars `DATABASE_URL` and `REDIS_URL`)
- copy and tweak variables `OTREE_` and `SECRET_KEY` from `deploy.env` into heroku app config apps
- build image with `docker build .` or `docker-compose build`
- tag image `docker tag IMAGENAME registry.heroku.com/APPNAME/web`
- do `heroku login`, `heroku container:login`
- push image to heroku `docker push registry.heroku.com/APPNAME/web`
- release container `heroku container:release web -a APPNAME`
- from online console run `otree resetdb`

### OtreeHub

- create an app on Heroku
- make `SECRET_KEY` config var with some random value
- register the app at OtreeHub
- configure everything in `Configure` tab
- build and start local production container `docker-compose up -d` (config and database don't matter)
- create package of the app `docker-compose exec web otree zip`
- copy the file from container to local dir `docker cp CONTAINERNAME:/app/app.otreezip .`
- upload the file to otreehub via `Deploy` tab
- reset db
