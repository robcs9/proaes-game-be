FROM python:alpine3.21

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir /usr/share/geojson /code/app

ENV GEOAPIFY_API_KEY=${GEOAPIFY_API_KEY}

CMD [ "python3", "main.py" ]