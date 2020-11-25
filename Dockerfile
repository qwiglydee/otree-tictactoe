#### development target

FROM python:3.8-slim AS devel
ARG USERUID=1000
ARG USERGID=1000

RUN addgroup --gid $USERGID devuser && adduser --uid $USERUID --ingroup devuser --home /work --shell /bin/bash --disabled-password devuser

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
 && apt-get -y install --no-install-recommends \
 build-essential \
 python3-dev \
 libpq5 \
 libpq-dev \
 git

COPY requirements*.txt /work

# NB: installing as root, globally
RUN pip install -r /work/requirements.txt
RUN pip install -r /work/requirements.devel.txt

ENV PATH /work/.local/bin:$PATH
WORKDIR /work
USER devuser:devuser

# MOUNT . /app  # from docker-compose or IDE

CMD otree devserver $PORT


#### demo-production target

FROM devel

RUN addgroup --system appuser && adduser --system --ingroup appuser --home /app --shell /bin/bash --disabled-password appuser

# TODO: only copy files from devel

ENV PATH /app/.local/bin:$PATH
WORKDIR /app
USER appuser:appuser

COPY --chown=appuser:appuser . .

# PORT will be redefined by Heroku
ENV PORT=8000
CMD otree prodserver $PORT
