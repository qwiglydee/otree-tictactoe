#### base layer

FROM python:3.8-slim AS base
ARG USERUID=1000
ARG USERGID=1000

RUN addgroup --system --gid $USERGID theuser && adduser --system --uid $USERUID --ingroup theuser --home /app --shell /bin/bash --disabled-password theuser

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
 && apt-get -y install --no-install-recommends \
 libpq5


#### building requirements

FROM base AS build

RUN apt-get -y install --no-install-recommends \
 build-essential \
 python3-dev \
 libpq-dev

COPY requirements*.txt /app

RUN pip install -r /app/requirements.txt


#### development target

FROM build AS devel

ENV PYTHONDONTWRITEBYTECODE 0

RUN apt-get -y install --no-install-recommends \
 git sqlite3

RUN pip install -r /app/requirements.devel.txt

# override with bind mount
COPY --chown=theuser:theuser . /app

WORKDIR /app
USER theuser:theuser

# override with `sleep`
CMD otree devserver 0.0.0.0:$PORT


#### demo target

FROM base as demo

COPY --from=build /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --chown=theuser:theuser . /app

WORKDIR /app
USER theuser:theuser

# PORT will be redefined by Heroku
ENV PORT=8000
CMD otree devserver 0.0.0.0:$PORT


#### production target

FROM base as prod

COPY --from=build /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --chown=theuser:theuser . /app

WORKDIR /app
USER theuser:theuser

# PORT will be redefined by Heroku
ENV PORT=8000
CMD otree prodserver 0.0.0.0:$PORT
