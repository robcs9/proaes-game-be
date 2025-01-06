from enum import Enum
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import json
import uvicorn

class ModelName(str, Enum):
  alexnet = "alexnet"
  resnet = "resnet"
  lenet = "lenet"

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static", name="static"))

@app.get("/api")
async def root():  
  return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
  return {"item_id": item_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
  if model_name is ModelName.alexnet:
    return {"model_name": model_name, "message": "Deep Learning FTW"}
  if model_name.value == "resnet":
    return {"model_name": model_name, "message": "LeCNN all the images"}
  if model_name.value == ModelName.lenet.value:
    return {"model_name": model_name, "message": "Le another Learning Model"}
  return {"message": "Oops!"}

# @app.get("/files/{file_path:path}")
# async def read_file(file_path: str):
    # return {"file_path": file_path}

@app.get("/api/geojson")
async def geojson():
  print("Opening data.geojson")
  try:
    with open('../data/data.geojson', encoding="utf-8") as file:
      print("GeoJSON found")
      content = file.read()
      geojson = json.loads(content)
      return {"data": geojson}
  except Exception as e:
    return { "error": "Falha ao recuperar o arquivo GeoJSON."}

# if __name__ == "__main__":
  # uvicorn.run("main:app", host="0.0.0.0", port=3000)

# run on custom port: $ uvicorn main:app --host 0.0.0.0 --port 3000