# Otree sample game


Dockerfile

docker-compose.devel.yaml

docker-compose.yaml

deploy.env

.devcontainer.json


## Local development


## Deployment

### Stand-alone server

- copy `deploy.env` into `.env` and tweak parameters
- `docker-compose up -d` -- to build and start everything

For first run:
- `docker-compose exec web otree resetdb` -- to initialize database
- `docker-compose restart web` -- restart after database init


### Heroku

...

### OtreeHub

...