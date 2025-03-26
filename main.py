from enum import Enum
from fastapi import FastAPI, BackgroundTasks
# from fastapi.staticfiles import StaticFiles
import json, uvicorn, time, os, sys, dotenv
import boto3
import dynamodb

sys.path.append('./app')
import app.main as scraper
import app.supabase_utils as supa_utils

API_V1 = "/api/v1"
DATA_PATH = './data'

# to-do: replace with importing of the env var for DATA_PATH
if os.getcwd().find('code') > -1:
  # sys.path.append('/code/app')
  DATA_PATH = './shared'
else:
  sys.path.append('./app')
  # import app.main as scraper

app = FastAPI()


# app.mount("/static", StaticFiles(directory="static", name="static"))
@app.get(API_V1)
async def root():  
  return {"message": "Welcome! Please, access /docs to learn more about this API."}

@app.get(f'{API_V1}/scrape')
def scrapeAds():
  scraper.main()
  return { "msg": "Scrape request received." }
  
UPDATED = False
@app.get(f'{API_V1}/db/geojson')
def readGeojsonFromDB():
  print('Reading geojson data from db now...')
  try:
    # geojson = json.loads(dynamodb.getGeojson())
    geojson = supa_utils.getGeojson()
    return geojson
  except Exception as e:
    return {
      'error': 'Failed to retrieve geojson data from the database'
    }

@app.get(f"{API_V1}/geojson")
async def geojson():
  print("Opening data.geojson")
  
  try:
    with open(f"{DATA_PATH}/data.geojson", encoding="utf-8") as file:
      print("GeoJSON found")
      content = file.read()
      geojson = json.loads(content)
      return {"data": geojson}
  except Exception as e:
    shared_path = os.path.abspath(f'{DATA_PATH}/data.geojson')
    print(f"Error.\n{e}\nPath: {shared_path}")
    msg = ""
    err = "No such file or directory"
    if str(e).find(err) != -1:
      msg = "Arquivo não encontrado"
    return { "error": f"Falha ao recuperar os dados GeoJSON. {msg}"}