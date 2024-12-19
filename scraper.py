import sys
import pandas as pd
from bs4 import BeautifulSoup
import json
import math
import codecs
from curl_cffi import requests as curlrq
import time
import asyncio
import re
import geoservices
import utils
from model import Ad
import repository as repo
import plot
# mostly constants
url_olx = "https://www.olx.com.br/imoveis/aluguel/estado-pe/grande-recife/recife?pe=1000&ret=1020&ret=1060&ret=1040&sd=3747&sd=3778&sd=3766&sd=3764&sd=3762"
url_wq = "https://www.webquarto.com.br/busca/quartos/recife-pe/Cordeiro%7CV%C3%A1rzea%7CTorre%7CTorr%C3%B5es%7CMadalena%7CIputinga?price_range%5B%5D=0,1000&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0"
url_mgf = "https://www.mgfimoveis.com.br/aluguel/quarto/pe-recife-cidade-universitaria?pricemax=1000"

# check if an ad already exists
def compareAds(ad: dict, prev_df):
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

def makeSoup(url: str):
    content = curlrq.get(url, impersonate="chrome")
    soup = BeautifulSoup(content.text, "lxml")
    return soup

# Retorna a quantidade de páginas de resultados da busca
def findPagePropsOLX(soup):
    data_str = soup.find("script", {"id": "__NEXT_DATA__"}).get_text()
    props = json.loads(data_str)['props']['pageProps']
    return props

# Bottleneck here
def getCepOLX(url: str):
    soup = makeSoup(url)
    data_str = soup.find('script', string=re.compile(r'(?:dataLayer = )(\[(.*)\])')).get_text(strip=True)    
    return re.search(r'"zipcode":"(\d{8})"', data_str).group(1)

def parseAddress(cep: str):
    res = curlrq.get(f'viacep.com.br/ws/{cep}/json/').json()
    if res.get('erro'):
        return 'Endereço com CEP inválido.'
    return f'{res['logradouro']}, {res['bairro']}, {res['localidade']}'

def searchOLX():
    soup = makeSoup(url_olx)
    page_props = findPagePropsOLX(soup)
    pages_count = math.ceil(page_props['totalOfAds'] / page_props['pageSize'])
    
    ads = []
    unfiltereds = []
    for i in range(1, pages_count + 1):
        data = {}
        # Evita a repetição do scraper na página inicial
        if i == 1:
            data = page_props['ads']
        else:
            page_url = f'{url_olx}&o={i}'
            soup = makeSoup(page_url)
            page_props = findPagePropsOLX(soup)
            data = page_props['ads']
        unfiltereds.append(data)
        print(f"Got OLX page {i} data")
        
    # Flattening nested lists with raw data, not only ads data
    unfiltereds = [ad for page in unfiltereds for ad in page]
    # filtereds = unfiltereds
    
    # todo - replace csv for json, then sqlite database eventually?
    # Load previous ads
    # prev_ads = repo.getAds()
    # filtereds = filterAds(unfiltereds, prev_ads)
    
    # update urls scraped that match any saved ad:
    # Either remove ads that are missing 'subject' key from the data file or Update fields that might have changed
    # todo (maybe?) - flag updatable ads to not go through the parseCoords function unless CEP has changed
    # todo - delete ads with broken url - def removeInvalidAds(); investigate if missing 'subject' key sufficies this check
    
    print('Processing ad data...')
    # print(unfiltereds)
    ceps = []
    unfiltereds_count = len(unfiltereds)
    invalid_count = 0
    # unfiltereds => unfiltered raw data, actually
    for i, ad in enumerate(unfiltereds):
        if ad.get("subject") is not None:
            cep = getCepOLX(ad['url'])
            cep = geoservices.normalizeCep(cep)
            addr = parseAddress(cep)
            # coords = geoservices.parseCoords(cep)
            # coords_split = coords.split(',') if len(coords) > 0 else [' ', ' ']
            
            ad_data = {
                'url': ad['url'], 
                'title': ad['subject'],
                'price': ad['price'],
                'address': addr if addr != 'Endereço com CEP inválido.' else ad['location'],
                'property_type': ad['category'],
                'cep': cep, # ignore or remove this attr once lat and lng are appended to the dict
            }
            
            try:
                cep_recorded = True if ceps.index(cep) else False
                print(f'Skipping CEP {cep}' if cep_recorded else '???')
            except Exception as e:
                cep_recorded = False
            if not cep_recorded:
                ceps.append(cep)
            # print(f'ceps state:\n{ceps}')
            
            ads.append(ad_data)
        else:
            # skip bad results scraped
            invalid_count += 1
            print(f'\nInvalid data (unfiltered) #{i}:\n{ad}\n')
        print(f"{i+1}/{unfiltereds_count} items have been processed")
    
    # todo - check if currently saved ads have changed
    # validateSavedData()
    
    coords = geoservices.batchGeocode(ceps)
    
    if coords is None:
        raise Exception('Erro. Falha na operação de Geocoding - Nenhum resultado obtido')

    geocoding_count = len(coords)
    # SEVERE BOTTLENECK
    # quick-fix: implement hashmap like: [{'ACTUAL_CEP': GEOCODE_DICT}, ...]
    # e.g. [..., {...}, {'12345-123': latlng_dict}, {...},...]
    print('Assinging geocodes to ads now...')
    proper_ads = []
    for i, ad in enumerate(ads):
        for coord in coords:
            
            if ad.get('cep'):
                if ad['cep'] == coord['cep']:
                    ad['lat'] = coord['lat']
                    ad['lng'] = coord['lng']
                else:
                    geocode = geoservices.toGeocode(ad['address'])
                    if not (geocode['lat'] == '' and geocode['lng'] == ''):
                        geocoding_count += 1
                    ad['lat'] = geocode['lat']
                    ad['lng'] = geocode['lng']
                ad.pop('cep')
        proper_ads.append(ad)
        print(f'{i}/{len(ads)} assigned')
    
    print(f'Total scraped ad links: {len(ads)}')
    # print(f'Geocoded CEPs: {len(coords)}/{ads_count}')
    print(f'Geocoded CEPs: {geocoding_count}/{len(ads)}')
    print(f'Invalid ads: {invalid_count};')
    print(f'Collected {len(proper_ads)} OLX ads')
    return proper_ads


def normalizeAdsPrices(ads: list[dict]):
    
    for ad in ads:
        price = ad['price']
        price = f'{price},00' if price.find(',') == -1 else price
        ad['price'] = price    
    
    return ads

def saveData(df: pd.DataFrame):
    df.to_json("data/data.json", columns=['Título', 'Tipo', 'Endereço', 'Preço', 'URL', 'lat', 'lng'])
    
    df = df.rename(columns={
        'url': 'URL', 'title': 'Título','thumbnail': 'Foto',
        'price': 'Preço','address': 'Endereço','property_type': 'Tipo',
        # 'latlng': 'Coordenadas'
    })
    # print(df.apply(lambda x: normalizeAdsPrices(x), axis=1, result_type='expand'))
    # print(df['Preço'])
    df.to_csv("data/data.csv", columns=['Título', 'Tipo', 'Endereço', 'Preço', 'URL', 'lat', 'lng'])

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

# main
async def main():
    running = True
    while running:
        validateSavedData()
        curr_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        print(f"\nScraping now... ({curr_time})\n")
        # dfWQ = utils.makeDataFrame(searchWQ())
        # dfOLX = utils.makeDataFrame(searchOLX())
        
        # olx_ads = searchOLX()
        # dfOLX = repo.saveAll(searchOLX)
        repo.saveAll(searchOLX())
        
        # searchWQ corrections pending
        # dfWQ = repo.saveAll(searchWQ)
        
        curr_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        print(f"\nScraping finished ({curr_time})\n")
        
        # plot.plotMap()
        break
        
        # Runtime loop
        # await asyncio.sleep(3600) # secs
        for i in range(10, 0, -1):
            print(f"Restarting in {i} secs...")
            await asyncio.sleep(1)
        print('Restarting now!')

asyncio.run(main())
# [O.K] - for tests only
# with open('./data/olx_ads_testbase.json') as fd:
#     olx_ads = json.load(fd)['olx_ads']
