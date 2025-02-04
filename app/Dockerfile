# FROM python
FROM python:alpine3.21

WORKDIR /usr/app

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

RUN mkdir ./app

CMD [ "python3", "./main.py" ]