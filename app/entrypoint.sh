#!/bin/sh

# New CMD: crontab running the main script and copying 
# the data.geojson to /usr/share/geojson/ right after


# crontab -l
# cat /etc/crontabs/root
# ls /etc/cron.d
# crond
echo "Running scraper python script now..."
python3 /code/main.py #&& cp /code/data/data.geojson /usr/share/geojson/