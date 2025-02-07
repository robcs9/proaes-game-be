# FROM python
FROM python:alpine3.21

# WORKDIR /usr/app
WORKDIR /code

COPY requirements.txt requirements.txt

# RUN apt update
# RUN apk add gdal gdal-dev proj proj-dev
RUN apk add build-base geos geos-dev && \
    export GEOS_LIBRARY_PATH=/usr
RUN pip install shapely
RUN pip3 install --no-cache-dir -r requirements.txt
# RUN sudo apt install python3-pip

# pipx for virtualenv with WSL!
# RUN sudo apt install python3 python3-pip pipx
# pipx install pandas --include-deps

COPY . .

# fixing .env file path (should be using env PATH vars to avoid using the commands below)
RUN mkdir ./app && \
    cp ./.env ./app/

# this doesn't work because the volume "shared" is not available yet
# RUN cp ./data/data.geojson ./shared
RUN mkdir /usr/share/geojson && \
    cp ./data/data.geojson /usr/share/geojson/

# New CMD: crontab running the main script and copying 
# the data.geojson to /usr/share/geojson/ right after
# CMD ["sh", "entrypoint.sh"]
# CMD [ "python3", "./main.py" ]
