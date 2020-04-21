FROM python:3.6-slim-stretch
ENV PYTHONUNBUFFERED 1

ARG ARG_VERSION_MAJOR
ARG ARG_VERSION_MINOR
ARG ARG_VERSION_PATCH
ARG ARG_RELEASE

ARG DEFAULT_USER

RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install supervisor -y \
    && apt-get install -y redis-server \
    && apt-get autoremove --purge \
    && apt-get clean
RUN set -x \
    && mkdir -p /srv/thelma \
    && mkdir -p /srv/thelma/app


COPY requirements.txt /srv/thelma/
WORKDIR /srv/thelma
RUN set -x \
    && pip3 install -r requirements.txt \
    && rm -rf /root/.cache

COPY thelma_project /srv/thelma/app/thelma

ADD entrypoint.sh /entrypoint.sh
RUN set -x \
    && chmod +x /entrypoint.sh

ENV VERSION_MAJOR ${ARG_VERSION_MAJOR}
ENV VERSION_MINOR ${ARG_VERSION_MINOR}
ENV VERSION_PATCH ${ARG_VERSION_PATCH}
ENV RELEASE       ${ARG_RELEASE}
ENV DEFAULT_USER ${DEFAULT_USER}
ENV API_ACCESS_TOKEN=unknown

WORKDIR /srv/thelma/app/thelma/config
RUN set -x && python -c "\
import pickle;\
import os;\
version = { 'VERSION_MAJOR': os.environ['VERSION_MAJOR'], 'VERSION_MINOR': os.environ['VERSION_MINOR'], 'VERSION_PATCH': os.environ['VERSION_PATCH'], 'RELEASE': os.environ['RELEASE']};\
pickle_file = open('version.pickle', 'wb');\
pickle.dump(version, pickle_file);\
pickle_file.close();"

EXPOSE 8002

WORKDIR /srv/thelma/app/thelma

ENTRYPOINT ["/entrypoint.sh"]