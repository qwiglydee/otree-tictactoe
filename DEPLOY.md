## Dockerization

The overall application is containerized using Docker to simplify deployment and development.
It is not required for deployment to Heroku or OtreeHub.

- `Dockerfile` contains commands to install and run everything in container.
  It has several stages/targets:
  - `base` -- basic requirements
  - `build` -- lots of stuff to build and install all required python modules
  - `devel` -- includes a few additional tools for development
  - `prod` (default) -- contains only what is needed to run the app in production (excluding building/developing stuff)
  - `demo` -- the same as `prod` but runs `otree devserver`
- `docker-compose.yaml` -- configuration to run the application on stand-alone server
- `docker-compose.devel.yaml` -- configuration to run container for development
- `deploy.env` -- meta-configuration parameters to run the server or developing container.
  The parameters should be copied to file `.env` or to `Config Vars` section on Heroku.


## Local development

A container for local development is configured in file `docker-compose.devel.yaml`.
It can be run with command `docker-compose`

### Bare sources

- Copy `deploy.env` to `.env` and tweak parameters (mainly `USERUID` and `USERGID`)
- Comment out line about sleep command in `docker-compose.devel.yaml`
- Run `docker-compose -f docker-compose.devel.yaml build` to build it
- Run `docker-compose -f docker-compose.devel.yaml up -d` to start it with `otree devserver`
- Local directory is mounted into container
- Server should be accessible via port 8000: `http://localhost:8000/`
- The `devserver` should notice changes in some sources and auto reload server

### VSCode

The IDE VSCode has add-on 'Remote container' that can open files, run commands, and debug code inside a docker container.
Files `.devcontainer.json` and directory `.vscode` contain configuration for VSCode and the addon.

- Copy `deploy.env` to `.env` and tweak parameters (mainly `USERUID` and `USERGID`)
- Uncomment out line about sleep command in `docker-compose.devel.yaml`
- Open working directory in VSCode
- Run command 'Reopen in Container'
- Use Ctrl/Shift-F5 to run/restart/debug `otree devserver`
- Ports are mapped weirdly, need to check 'Remote explorer` tab to figure out correct port. Sometimes the mapping should be deleted and recreated.

## Stand-alone deployement

Running the app in production requires 2 additional database servers.
They are configured in `docker-compose.yaml` to autostart with `docker-compose`.

- Copy `deploy.env` to `.env` and tweak parameters (mainly, uncomment `DATABASE_URL`, `REDIS_URL` and some otree stuff)
- Maybe, adjust `docker-compose.yaml` for restarting policy
- Run `docker-compose build` to build it
- Run `docker-compose up -d` to start everything
- Run `docker-compose exec web otree resetdb` to reset database

## Heroku docker deployment

- Create an application on Heroku
- Attach addons 'Heroku Postgres' and 'Heroku Redis' from addon market. This will automatically put correct config vars for the application
- In config vars create `SECRET_KEY` with random value, and `OTREE` vars from `deploy.env`
- Do `heroku login` and `heroku container:login`
- `docker build --target prod -t APPNAME:prod .` to build production container
- `docker tag APPNAME:prod registry.heroku.com/APPNAME/web`
- `docker push registry.heroku.com/APPNAME/web`
- `heroku container:release web -a APPNAME`

## Heroku git deployment

- Create an application on Heroku
- Attach addons 'Heroku Postgres' and 'Heroku Redis' from addon market. This will automatically put correct config vars for the application
- In config vars create `SECRET_KEY` with random value, and `OTREE` vars from `deploy.env`
- Add git remote `heroku https://git.heroku.com/APPNAME.git`
- Push sources to the remote
- Heroku will build and run everything automatically
- From Heroku app console run `otree resetdb` to reset database

Also, it probably needs email service.

## Otreehub deployment

- Create an application on Heroku
- In config vars create `SECRET_KEY` with random value
- Register it on otreehub
- Configure everything in 'Configure' tab
- Package source files with `otree zip`
- Upload the archive to otreehub
- Reset db

The utility `otree zip` is not very smart and it can pick up some development files like caches and VSCode container-related stuff (which is quite huge). Such stuff should be cleaned up before ziping.
