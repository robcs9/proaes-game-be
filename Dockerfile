# FROM python:3.9
FROM python:alpine3.21

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./app /code/app
# COPY . /code/app
COPY . .

# AWS config steps
# RUN cp -r /code/app/.aws /code/
# RUN source ./app/.aws/credentials


# Render-exclusive steps
# CMD [ "ls", "-alh", "/etc/secrets" ] # to-do: implement path to the .env from this directory
RUN cp /etc/secrets/.env /code/


CMD ["fastapi", "run", "main.py", "--port", "8123"]

EXPOSE 8123

# If running behind a proxy like Nginx or Traefik add --proxy-headers e.g.:
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]