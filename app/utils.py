from bs4 import BeautifulSoup
import repository as repo
# from urllib.request import urlopen
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import time
# import requests as rq
# from io import StringIO

url = "https://www.olx.com.br/imoveis/aluguel/estado-pe/grande-recife/recife?pe=2000&ret=1020&ret=1060&ret=1040&sd=3747&sd=3778&sd=3766&sd=3764&sd=3762&o=2"
# headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

def search(url):
    # from curl_cffi import requests as currq
    # res = currq.get(url, impersonate="chrome")
    # soup = BeautifulSoup(res.text, 'lxml')
    soup = makeSoup(url)
    print(soup.find('script', {"id": "__NEXT_DATA__"}).get_text())


# from selenium import webdriver
def makeSeleniumSoup(url):
    driver = webdriver.Firefox()
    driver.get(url)
    content = driver.page_source.encode("utf-8").strip()
    soup = BeautifulSoup(content, "lxml") # alt parser: html.parser
    return soup

import pandas as pd

def normalizeAdsPrices(ads: list[dict]):
    
    for ad in ads:
        price = ad['price']
        price = f'{price},00' if price.find(',') == -1 else price
        ad['price'] = price    
    
    return ads

def makeDataFrame(data_arr: list):
    data_arr = normalizeAdsPrices(data_arr)
    
    serieses = []
    
    # print(f"Anúncios de Moradia encontrados na {src}:")
    for data in data_arr:
        s = pd.Series(data)
        serieses.append(s)
        # print(f"\n{s}\n")
    
    df = {}
    df = pd.DataFrame(serieses)
    return df
    # for i, data in enumerate(data_arr):    
    
    # print(data_arr[0])
    # df = pd.DataFrame({some_series: pd.Series.keys some_series.title}, index = some_series.index)
    # print(df)

from datetime import datetime
def dateTimeNow():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


# Refactoring for modular structure section

# check if an ad already exists
def compareAds(ad: dict, df):
    if ad.get('url'):
        found = repo.find(ad['url'])
        return True if len(found) > 0 else False
    print('Error: ad url empty or invalid')

# Filters out ads sharing the same url
# todo: test behavior for empty and equal ads arrays
def filterAds(new_ads: list[dict], prev_df):
    
    print(f'Filtering out ads...\n {len(new_ads)} ads to be matched against the {len(prev_df)} previously stored ads')
    # updatable_ads = []
    for i, ad in enumerate(new_ads):
        # if compareAds(ad, prev_df.get('url')):
        idx = repo.find(ad['url']).index[0]
        repo.update(ad, idx)
        # new_ads.pop() - pop current ad, but missing arg (actual index for ad)
        # if compareAds(ad, prev_df):
        #     repo.update(ad, idx)
    return new_ads

from curl_cffi import requests as curlrq
def makeSoup(url: str):
    try:
        content = curlrq.get(url, impersonate="chrome")
        soup = BeautifulSoup(content.text, "lxml")
    except Exception as e:
        print(f"Erro durante scraping da url ({url}).\n{e}")
        return
    return soup

def parseAddress(cep: str):
    # find alternative to ViaCEP for downtimes
    if cep is None or len(cep) < 8:
        print(f"Falha ao tentar processar CEP inválido ({cep}).")
        return
    # res = curlrq.get(f'https://viacep.com.br/ws/{cep}/json/').json()
    res = curlrq.get(f'opencep.com/v1/{cep}').json()
    # if res.get('erro'): # ViaCep error response
    if res.get('error'):
        print(f"Endereço não encontrado para o CEP informado ({cep}).")
        return
    return f'{res['logradouro']}, {res['bairro']}, {res['localidade']}'

def normalizeAdsPrices(ads: list[dict]):
    
    for ad in ads:
        price = ad['price']
        price = normalizePrice(price)
        ad['price'] = price    
    
    return ads

def normalizePrice(price: str):
    return f'{price},00' if price.find(',') == -1 else price

# Checa se as páginas dos ads salvos ainda estão disponíveis na OLX
def validateSavedData():
    print('\nValidating status for previously saved ads')
    ads_df = repo.getAds()
    urls = ads_df.get('url')
    ads_df_len = len(urls) if urls is not None else 0
    if ads_df_len == 0:
        print('\nNo ads previously saved found. Skipping validation.')
        return
    
    count = len(urls)
    for i,url in enumerate(urls):
        res = curlrq.get(url, impersonate='chrome')
        status_code = res.status_code
        if status_code >= 400 and status_code < 500:
            print(f'\nAd with URL {url} not available anymore. Removing now...')
            idx = ads_df[ads_df['url'] == url].index[0]
            repo.delete(idx)
        # else: make ad active again?
        print(f'\nValidated ads: {i+1}/{count}')

def normalizeCep(cep: str):
    if cep.find('-') > -1:
        cep = ''.join(cep.split('-'))
    return cep

# check for the correct path
# print(Path.cwd())
# print(Path('./app/data/data.geojson').resolve(strict=True))

# FastAPI
# listening on custom PORT
# if __name__ == "__main__":
  # uvicorn.run("main:app", host="0.0.0.0", port=3000)

# run on custom port. default host: 127.0.0.1, default port: 8000
# $ uvicorn main:app --host 127.0.0.1 --port 3000