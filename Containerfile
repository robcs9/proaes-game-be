FROM python

WORKDIR /usr/app

COPY requirements.txt requirements.txt

# RUN apt update
RUN pip3 install --no-cache-dir -r requirements.txt
# RUN sudo apt install python3-pip

# pipx for virtualenv with WSL!
# RUN sudo apt install python3 python3-pip pipx
# pipx install pandas --include-deps

COPY . .


# CMD [ "fastapi", "dev", "./api/main.py" ]
CMD [ "python3", "./main.py" ]

# RUN python3 ./main.py
# Requires multithreading through bash scripting to run both API and scraper OR running detached containers
# CMD [ "fastapi", "dev", "./api/main.py" ]

# EXPOSE 8000