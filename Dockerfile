FROM python:3-alpine

ENV PYLIPS_VERISON master

RUN apk add --virtual build-tools unzip gcc g++ make openssl-dev python3-dev

RUN mkdir -p /opt/pylips/

WORKDIR /opt/pylips/

ADD https://github.com/eslavnov/pylips/archive/${PYLIPS_VERISON}.zip pylips.zip

RUN unzip pylips.zip && rm pylips.zip && mv pylips-*/* .

RUN pip install -r requirements.txt

RUN apk del build-tools

ENTRYPOINT python /opt/pylips/pylips.py

