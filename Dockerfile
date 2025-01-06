# > python:3.12
FROM python:3.11-slim

# WORKDIR /usr/src/app
WORKDIR /usr/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

# CMD [ "fastapi", "dev", "./api/main.py"]
CMD [ "python", "./main.py"]
