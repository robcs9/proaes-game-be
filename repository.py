# todo - sqlite implementation

import pandas as pd
import os.path as path
import utils
# todo - use Ad class for dicts
from model import Ad

ATTRS = ['id', 'title', 'price', 'address', 'url', 'property_type', 'modifiedAt','active', 'lat', 'lng',]

# Initializes empty DataFrame properly and saves it to CSV
def initDF():
  # attrs = Ad.__dict__['__static_attributes__']
  df = pd.DataFrame(columns=ATTRS)
  df.set_index('id', inplace=True)
  # df.to_csv('./data/data.csv')
  # pd.concat([df, new_df], ignore_index=True)
  print('New empty DataFrame for ads initialized successfully')
  return df

# def getAds(active=True) - rewrite to allow choice of ads active or not
def getAds():
  # if path.exists('./data/data.csv'):
  file_name = 'data.csv'
  ads_df = initDF()
  try:
    ads_df = pd.read_csv(f'./data/{file_name}', index_col=0)
    print('Ads retrieved successfully')
  except FileNotFoundError as e:
    print(f'\nError: {e.strerror}. Arquivo CSV {file_name} não encontrado\n')
  print(f'{len(ads_df)} ads retrieved')
  return ads_df

# import numpy as np
# try np.where?
def save(ad: dict):
  ads_df = getAds()
  
  found = ads_df.loc[ads_df['url'] == ad['url']]
  if len(found) > 0:
    # todo - handle multiple search hits
    print('Similar ad(s) have been found. Updating instead now...')
    # ad['id'] = int(found.index[0])
    idx = int(found.index[0])
    return update(ad, idx)
  
  idx = ads_df.last_valid_index()
  idx = 0 if idx is None else idx + 1
  for k, v in ad.items():
    ads_df.loc[idx, k] = v
  ads_df.loc[idx, 'modifiedAt'] = utils.dateTimeNow()
  ads_df.loc[idx, 'active'] = True
  
  # ads_df.to_json('./data/data.json',force_ascii=False)
  ads_df.to_csv('./data/data.csv')
  print('New ad saved!')
  last_ad = ads_df.tail(1)
  print(last_ad)
  return last_ad

# Saves into new file or appends to current file
def saveAll(ads: list[dict]):
  ads_df = getAds()
  if len(ads_df) > 0:
    for ad in ads:
      save(ad)
    print('All ads appended to data.csv successfully')
    return
  
  # df = utils.makeDataFrame(ads)
  # df.to_csv('./data/data.csv')
  # print('save op msg2')

# def saveAll(ads_df: pd.DataFrame):

def find(url: str):
  ads_df = getAds()
  found = pd.Series()
  try:
    found = ads_df.loc[lambda df: df['url'] == url]
    print(f'{len(found)} ads found')
  except Exception as e:
    print(f'\nError: Ad com URL informada ({e}) não encontrado.\n')
  return found


def update(updated_ad: dict, idx: int):
  ads_df = getAds()
  wasUpdated = False
  for k, v in updated_ad.items():
    # idx = updated_ad['id']
    keyExists = None
    try:
      keyExists = ATTRS.index(k)
    except Exception as e:
      print(f'Error: Key {k} not recognizable as ad attribute field. Skipping...')
    
    prev_v = ads_df.loc[idx, k]
    if keyExists is not None and prev_v != v:
      ads_df.loc[idx, k] = v
      ads_df.loc[idx, 'modifiedAt'] = utils.dateTimeNow()
      print(f'{k} field updated!')
      wasUpdated = True
  
  if wasUpdated:
    # ads_df.to_json('./data/data.json',force_ascii=False)
    ads_df.set_index('id', inplace=True)
    ads_df.to_csv('./data/data.csv')
    print(ads_df)
  else:
    print('There were no updates to be performed.')

def delete(url: str):
  ads_df = getAds()
  found = find(url)
  if found is not None:
    idx = found.index[0]
    ads_df.loc[idx, 'active'] = False
    ads_df.loc[idx, 'modifiedAt'] = utils.dateTimeNow()
    print(f'Ad with id {idx} has been (soft) deleted successfully')
    print(ads_df.loc[idx])
    return
    
  print('Ad removal has failed')
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
# delete(real_url)
