FROM python

LABEL maintainer="rcs9@proton.me"

COPY dependencies.txt dependencies.txt

RUN pip3 install -r dependencies.txt

# WORKDIR /usr/src/app

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD [ "fastapi", "dev", "./api/main.py"]
CMD [ "python3", "-m", "./main.py"]
