#!/bin/sh

echo 'Copying data.geojson to shared volume'
cp /code/data/data.geojson /usr/share/geojson/data.geojson
echo 'The data.geojson file has been updated!'