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
- `docker-compose exec web otree resetdb` -- to initialize database
- `docker-compose restart web` -- restart after database init


### Heroku

- create an app on heroku
- attach redis and postgres services (this should also create config vars `DATABASE_URL` and `REDIS_URL`)
- copy and tweak variables `OTREE_` and `SECRET_KEY` from `deploy.env` into heroku app config apps
- build image with `docker build .` or `docker-compose build`
- tag image `docker tag IMAGENAME registry.heroku.com/APPNAME/web`
- do `heroku login`, `heroku container login`
- push image to heroku `docker push registry.heroku.com/APPNAME/web`
- release container `heroku container:release web -a APPNAME`
- from online console run `otree resetdb `

TODO: something with Procfile and web/worker containers

### OtreeHub

...
