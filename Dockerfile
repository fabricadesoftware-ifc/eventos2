FROM python:3.7-stretch

RUN apt-get update && \
    apt-get install -yqq apt-transport-https curl git gnupg

RUN echo "deb https://deb.nodesource.com/node_12.x stretch main" > /etc/apt/sources.list.d/nodesource.list && \
    curl -sSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
    apt-get update && \
    apt-get install -yqq nodejs

RUN pip install poetry

RUN useradd --create-home appuser

USER appuser
