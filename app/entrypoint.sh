#!/bin/sh

echo "Copying .env file"
cp /run/secrets/env_secrets /code/app/.env
echo ".env updated!"
ls /code/app/
echo "Executing python scraper script now..."
python3 /code/main.py #&& cp /code/data/data.geojson /usr/share/geojson/