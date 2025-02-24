# FROM python
FROM python:alpine3.21

# WORKDIR /usr/app
WORKDIR /code

COPY requirements.txt requirements.txt

RUN apk add --update --no-cache build-base geos geos-dev openrc cronie && \
    export GEOS_LIBRARY_PATH=/usr
RUN pip install shapely 
RUN pip3 install --no-cache-dir -r requirements.txt

# AWS SDK
# RUN pip install --no-cache-dir boto3

COPY . .

# fixing .env file path (should be using env PATH vars to avoid using the commands below)
# RUN mkdir ./app && \
    # cp ./.env ./app/
    # cp /run/secrets/env_secrets ./app/.env

RUN mkdir /usr/share/geojson /code/app

# RUN cp ./.env /run/secrets/env_secrets
COPY ./crontab /etc/crontabs/root
RUN chmod +x ./entrypoint.sh ./update_shared_data.sh

CMD [ "busybox", "crond", "-l", "2", "-f" ]