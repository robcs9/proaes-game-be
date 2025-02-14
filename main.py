from enum import Enum
from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
import json, uvicorn, time, os
# import app.main as scraper

API_V1 = "/api/v1"
app = FastAPI()

# app.mount("/static", StaticFiles(directory="static", name="static"))
@app.get(API_V1)
async def root():  
  return {"message": "Hello!"}

# import app.main as scraper
@app.get(f'{API_V1}/scrape')
async def scrape():
  print('API calling scraper now')
  # scraper()
  return {'status code': 200}


# @app.get("/files/{file_path:path}")
# async def read_file(file_path: str):
    # return {"file_path": file_path}

@app.get(f"{API_V1}/geojson")
async def geojson():
  print("Opening data.geojson")
  
  # check for the correct path
  # print(Path.cwd())
  # print(Path('./app/data/data.geojson').resolve(strict=True))
  
  try:
    # with open("./data/data.geojson", encoding="utf-8") as file:
    with open("./shared/data.geojson", encoding="utf-8") as file:
      print("GeoJSON found")
      content = file.read()
      geojson = json.loads(content)
      return {"data": geojson}
  except Exception as e:
    shared_path = os.path.abspath('./shared/data.geojson')
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