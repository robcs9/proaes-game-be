# todo - sqlite implementation
import pandas as pd
import os, json
import os.path as path
from plot import scatterOverlaps
import utils as utils

# DATA_DIR = './data' # when running on local machine
# DATA_DIR = '/code/data' # when running on containers
DATA_PATH = os.path.join(os.getcwd(), 'data')
DATA_DIR = DATA_PATH if not os.getcwd() == '/root' else '/code/data'
ATTRS = ['id', 'title', 'price', 'address', 'url', 'property_type', 'modifiedAt','active', 'lat', 'lng',]

# Initializes empty DataFrame properly and saves it to CSV
def initDF():
  # attrs = Ad.__dict__['__static_attributes__']
  df = pd.DataFrame(columns=ATTRS)
  df.set_index('id', inplace=True)
  if not path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
  df.to_csv(f'{DATA_DIR}/data.csv')
  # pd.concat([df, new_df], ignore_index=True)
  print('\nNew empty DataFrame for ads initialized successfully')
  return df

def getAds(active_only=False):
  # if path.exists('./data/data.csv'):
  file_name = 'data.csv'
  
  try:
    ads_df = pd.read_csv(f'{DATA_DIR}/{file_name}', index_col=0)
    print('\nAds retrieved successfully')
  # except FileNotFoundError as e:
  except Exception as e:
    print(f'\nError: {e.strerror}. Arquivo CSV {file_name} não encontrado\n')
    ads_df = initDF()
  
  if active_only and len(ads_df) > 0:
    ads_df = ads_df[ads_df['active'] == True]
  
  print(f'\n{len(ads_df)} ads retrieved')
  return ads_df

# import numpy as np
# try np.where?
def save(ad: dict):
  ads_df = getAds()
  # idx = 0
  idx = len(ads_df)
  for k, v in ad.items():
    ads_df.loc[idx, k] = v
  ads_df.loc[idx, 'modifiedAt'] = utils.dateTimeNow()
  ads_df.loc[idx, 'active'] = True
  
  # ads_df.to_json('./data/data.json',force_ascii=False)
  ads_df.to_csv(f'{DATA_DIR}/data.csv',encoding='utf-8')
  print('\nNew ad saved!')
  last_ad = ads_df.tail(1)
  print(last_ad)
  return last_ad

def saveAdDF(ads_df: pd.DataFrame, ad: dict):
  # idx = 0
  idx = len(ads_df) + 1
  for k, v in ad.items():
    ads_df.loc[idx, k] = v
  ads_df.loc[idx, 'modifiedAt'] = utils.dateTimeNow()
  ads_df.loc[idx, 'active'] = True
  
  # ads_df.to_json('./data/data.json',force_ascii=False)
  # ads_df.to_csv('./data/data.csv',encoding='utf-8')
  print('\nNew ad saved!')
  last_ad = ads_df.tail(1)
  print(last_ad)
  return ads_df

# Saves into new file or appends to current file
def saveAll(ads: list[dict], dir=DATA_DIR):
  if ads is None:
    print(f'Error. No ads were provided. Ads:\n{ads}')
    return
  ads_df = initDF()
  # Remove previously saved data
  # print('Removendo dados salvos previamente')
  # try:
  #   os.remove('./data/data.csv')
  #   os.remove('./data/data.geojson')
  #   print('Removendo')
  # except Exception as e:
  #   print(f"Error:\n{e}")
    # handle error?

  for ad in ads:
    ads_df = saveAdDF(ads_df, ad)
  ads_df.to_csv(f"{dir}/data.csv",encoding='utf-8')
  print('\nAll ads saved to data.csv successfully')
  
  # Exporting to geojson as well
  # ads_df = getAds(active_only=True)
  ads_df = scatterOverlaps(ads_df)
  toGeojson(ads_df, dir)
  
  # ads_df = getAds()
  # if len(ads_df) > 0:
  #   for ad in ads:
  #     save(ad)
  #   print('All ads appended to data.csv successfully')
  #   return
  
  # df = utils.makeDataFrame(ads)
  # df.to_csv('./data/data.csv')
  # print('save op msg2')

# def saveAll(ads_df: pd.DataFrame):

def find(url: str):
  ads_df = getAds()
  found = pd.Series()
  try:
    found = ads_df.loc[lambda df: df['url'] == url]
    print(f'\n{len(found)} ads found')
  except Exception as e:
    print(f'\nError: Ad com URL informada ({e}) não encontrado.\n')
  return found


def update(updated_ad: dict, idx: int):
  ads_df = getAds()
  did_update = False
  for k, v in updated_ad.items():
    # idx = updated_ad['id']
    keyExists = None
    try:
      keyExists = ATTRS.index(k)
    except Exception as e:
      print(f'\nError: Key {k} not recognizable as ad attribute field. Skipping...')
    
    prev_v = ads_df.loc[idx, k]
    if keyExists is not None and prev_v != v:
      ads_df.loc[idx, k] = v
      ads_df.loc[idx, 'modifiedAt'] = utils.dateTimeNow()
      print(f'{k} field updated!')
      did_update = True
  
  if did_update:
    # ads_df.to_json('./data/data.json',force_ascii=False)
    # ads_df.set_index('id', inplace=True)
    ads_df.to_csv(f'{DATA_DIR}/data.csv')
    # print(ads_df)
  else:
    print('\nThere were no updates to be performed.')

def delete(idx: int):
  ads_df = getAds()
  # handle errors raised from iloc
  try:
    found = ads_df.iloc[idx]
  except Exception as e:
    print(f'\nError: {e}. Falha ao deletar ad.')
    return
  if found is not None:
    # idx = found.index[0]
    ads_df.loc[idx, 'active'] = False
    ads_df.loc[idx, 'modifiedAt'] = utils.dateTimeNow()
    ads_df.to_csv(f'{DATA_DIR}/data.csv')
    print(f'\nAd with id {idx} has been (soft) deleted successfully')
    return
  print('\nAd removal has failed')
  # copy/slice of a DF which is not settable
  # ads_df[ads_df['url'] == url]['lng'] = -9999900
  # ads_df.drop(find(url).index, inplace=True)
  # print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
  # print(ads_df)

# tests CONCLUDED
# real_url = 'https://www.webquarto.com.br/quarto/97678/quarto-individual-em-ape-na-av-caxanga'
# internally initialized fields not included: id, modifiedAt, active
# mock_ad = {
# 'title': 'a title',
# 'price': 'R$ 500',
# 'address': 'an address',
# 'url': real_url, #'url0',
# 'property_type': 'a property_type',
# 'lat': -42,
# 'lng': -99000,
# }
# initDF()
# ads = getAds()
# save(mock_ad)
# saveAll([mock_ad])
# res = find('https://www.webquarto.com.br/quarto/97678/quarto-individual-em-ape-na-av-caxanga')
# update(mock_ad)
# real_url = 'https://pe.olx.com.br/grande-recife/imoveis/apartamento-para-aluguel-1-quarto-1-vaga-cordeiro-recife-pe-1282369079'
# delete(1)

# todo - manage all .to_csv() calls with proper file opening mode (truncate, overwrite, append...)

def makeFeatures(df: pd.DataFrame):
  geo_features = []
  shape = {
    "type": "Feature",
    "properties": {
      "id": 0,
      "title": "",
      "price": "",
      "address": "",
      "url": "",
      "property_type": "",
      "modifiedAt": "",
      "active": "",
    },
    "geometry": {
      "type": "Point",
      "coordinates": [
        -56.0,
        -15.5
      ]
    }
  }
  
  if df is None:
    print('Error: Invalid DataFrame passed. Unable to make geojson features.')
    return geo_features
  
  keys = shape['properties'].keys()
  for i in df.index:
    feature = dict(type="Feature",properties={},geometry={"type": "Point"})
    feature['properties']['id'] = i
    feature['geometry']['coordinates'] = [df.loc[i, 'lng'], df.loc[i, 'lat']]
    for key in keys:
      if key != "id":
        feature['properties'][key] = df.loc[i, key]
      # if key == "active":
        # print(f'active status: {df.loc[i,key]}')
        # feature['properties'][key] = df.loc[i, key]
        # feature['properties'][key] = bool(shape['properties'][key])
        # debug: check if active is being set to "True" every time at this point
    feature['properties']['active'] = bool(feature['properties']['active'])
    geo_features.append(feature)
  
  # debugging/testing - remove after done
  # geo_features[0]['properties']['active'] = True
  return geo_features

def toGeojson(df:pd.DataFrame=None, dir=DATA_DIR):
  # import numpy as np
  # df['active'] = df['active'].astype('bool')
  # print(type(df.loc[1,"active"]))
  
  data = {
    "type": "FeatureCollection",
    "features": []
  }
    
  features = makeFeatures(df)
  # print(f'\nfeatures: {features} \n')
  
  data['features'] = features
  # checking proper bool type for active
  # print(type(data['features'][0]['properties']['active']))
  geojson = json.dumps(data, ensure_ascii=False)
  # geojson = json.dumps({'foo': 'bará'}, ensure_ascii=False,)
  try:
    with open(f"{dir}/data.geojson", 'w', encoding='utf-8') as fd:
      fd.write(geojson)
      print("GEOJSON saved successfully!")

  except Exception as e:
    print(f'Falha ao salvar geojson. Error: {e}. ')

def export():
  print('Scattering overlapping points and exporting geojson data now...')
  ads_df = getAds(active_only=True)
  ads_df = scatterOverlaps(ads_df)
  toGeojson(ads_df)

# export()