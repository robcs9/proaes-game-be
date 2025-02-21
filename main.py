from enum import Enum
from fastapi import FastAPI, BackgroundTasks
# from fastapi.staticfiles import StaticFiles
import json, uvicorn, time, os, sys
# import app.main as scraper
API_V1 = "/api/v1"
DATA_PATH = './data'

# to-do: replace with importing of the env var for DATA_PATH
if os.getcwd().find('code') > -1:
  # sys.path.append('/code/app')
  DATA_PATH = './shared'
else:
  sys.path.append('./app')
  import app.main as scraper

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static", name="static"))
@app.get(API_V1)
async def root():  
  return {"message": "Welcome! Please, access /docs to learn more about this API."}

@app.get(f'{API_V1}/scrape')
async def scrape():
  print('API calling scraper now')
  if scraper is not None:
    scraper.main()
  return { "msg": "API calling scraper now" }

@app.get(f"{API_V1}/geojson")
async def geojson():
  print("Opening data.geojson")
  
  # check for the correct path
  # print(Path.cwd())
  # print(Path('./app/data/data.geojson').resolve(strict=True))
  
  try:
    # with open("./data/data.geojson", encoding="utf-8") as file:
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

# listening on custom PORT
# if __name__ == "__main__":
  # uvicorn.run("main:app", host="0.0.0.0", port=3000)

# run on custom port. default host: 127.0.0.1, default port: 8000
# $ uvicorn main:app --host 127.0.0.1 --port 3000