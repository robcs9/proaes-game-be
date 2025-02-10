# FROM python
FROM python:alpine3.21

# WORKDIR /usr/app
WORKDIR /code

COPY requirements.txt requirements.txt

# RUN apt update
# RUN apk add gdal gdal-dev proj proj-dev
RUN apk add --update --no-cache build-base geos geos-dev openrc cronie && \
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

RUN mkdir /usr/share/geojson && \
    cp ./data/data.geojson /usr/share/geojson/

# RUN echo "*/1 * * * * echo 'Hi... again?'" >> /var/spool/cron/crontabs/root
# RUN echo "* * * * *    echo 'Hi... again?'" >> /etc/crontabs/root # flawed
# RUN echo "* * * * *    echo 'Hi... again?' >> /code/crontab_log.txt" >> /etc/crontabs/root # working

# CMD [ "python3", "./main.py" ]
# New CMD: crontab running the main script and copying 
# the data.geojson to /usr/share/geojson/ right after
# CMD ["sh", "entrypoint.sh"]
RUN echo "* * * * *    python3 /code/main.py >> /code/crontab_log.txt" >> /etc/crontabs/root
CMD [ "crond","-n" ]