FROM python:3-slim-bullseye

RUN apt-get update && \
apt-get install -y --no-install-recommends iputils-ping && \
rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY [^settings.ini]* .

ENTRYPOINT [ "python", "pylips.py" ]
