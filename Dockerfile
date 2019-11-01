FROM python:3-alpine

RUN apk add --virtual build-tools gcc g++ make openssl-dev python3-dev

RUN mkdir -p /opt/pylips/

WORKDIR /opt/pylips/

ADD ./ /opt/pylips/

RUN pip install -r requirements.txt

RUN apk del build-tools

ENTRYPOINT python /opt/pylips/pylips.py

