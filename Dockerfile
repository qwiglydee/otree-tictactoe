#### building

FROM python:3.8-slim AS build

ARG USERUID=1000
ARG USERGID=1000

RUN addgroup --gid $USERGID devuser && adduser --uid $USERUID --ingroup devuser --home /work --shell /bin/bash --disabled-password devuser

RUN apt-get update \
 && apt-get -y install --no-install-recommends \
 build-essential \
 python3-dev \
 libpq5 \
 libpq-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements*.txt /work

RUN pip install -r /work/requirements.txt


#### development target

FROM build AS devel

RUN apt-get -y install --no-install-recommends \
 git

RUN pip install -r /work/requirements.devel.txt

WORKDIR /work
USER devuser:devuser

COPY --chown=devuser:devuser . .

CMD otree devserver $PORT


#### production target

FROM python:3.8-slim as prod

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN addgroup --system appuser && adduser --system --ingroup appuser --home /app --shell /bin/bash --disabled-password appuser

RUN apt-get update \
 && apt-get -y install --no-install-recommends \
 libpq5

COPY --from=build /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

WORKDIR /app
USER appuser:appuser

COPY --chown=appuser:appuser . .

# PORT will be redefined by Heroku
ENV PORT=8000
CMD otree prodserver $PORT
