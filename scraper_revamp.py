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
    
    # Flattening nested lists with ads
    unfiltereds = [ad for page in unfiltereds for ad in page]
    # filtereds = unfiltereds
    print('Processing ad data...')
    
    # todo - replace csv for json, then sqlite database eventually?
    # Load previous ads
    # prev_ads = repo.getAds()
    # filtereds = filterAds(unfiltereds, prev_ads)
    
    total_ads_count = 0
    current_ads_count = 0
    # geoservices.batchGeocode()
    # update urls scraped that match any saved ad:
    # Either remove ads that are missing 'subject' key from the data file or Update fields that might have changed
    # todo (maybe?) - flag updatable ads to not go through the parseCoords function unless CEP has changed
    # todo - delete ads with broken url - def removeInvalidAds(); investigate if missing 'subject' key sufficies this check
    
    ceps = []
    for i, ad in enumerate(unfiltereds):
        if ad.get("subject") is not None:
            cep = getCepOLX(ad['url'])
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
            ceps.append(cep)
            ads.append(ad_data)
        # print(f"{i+1}/{total_ads_count} OLX ads have been processed")
    for ad in ads:
        coords = geoservices.batchGeocode(ceps)
        ad['lat'] = coords['lat']
        ad['lng'] = coords['lng']
        # remove cep attr from ad dict here
        continue
    print(f'All {len(unfiltereds)} ads processed')
    return
    current_ads_count = len(filtereds)
    # for i, ad in enumerate(updatables):
    #     # todo - def updateOlxAd(ad)
    #     if ad.get("subject") is not None:
    #         actual_ad = {
    #             'url': ad['url'], # don't update
    #             'title': ad['subject'],
    #             'thumbnail': ad['thumbnail'],
    #             'price': ad['price'],
    #             'address': addr if addr != 'Endereço com CEP inválido.' else ad['location'],
    #             'property_type': ad['category'],
    #             'latlng': coords, # get from prev_ads
    #             'lat': coords_split[0], # get from prev_ads
    #             'lng': coords_split[1], # get from prev_ads
    #             'active': True,
    #             'modifiedAt': utils.dateTimeNow()
    #         }
    #         ads.append(actual_ad)
    #     print(f"{current_ads_count+1+i}/{total_ads_count} OLX ads have been processed")
    
    return ads


# WQ multi-pages test url
# testing-only, keep commented out otherwise
# url_wq = "https://www.webquarto.com.br/busca/quartos/recife-pe?page=1&price_range[]=0,15000&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0"


def normalizeAdsPrices(ads: list[dict]):
    
    for ad in ads:
        price = ad['price']
        price = f'{price},00' if price.find(',') == -1 else price
        ad['price'] = price    
    
    return ads

def findDataWQ(raw):
    # target text between 'window.search' and 'window.search.city_name'
    for line in raw:
        content = line.get_text().strip()
        begin = "window.search = {"
        end = "window.search.city_name"
        if content.find(begin) > -1:
            end_idx = content.find(end)
            data_str = content[len(begin) - 1 : end_idx].strip()[:-1]
            rest_str = content[end_idx:]
            return data_str, rest_str
    return ""

def findPaginationWQ(src):
    arr = src.split(" = ")
    s = arr[3]
    end = s.find("window")
    s = s[:end - 4]
    return json.loads(s)

# Remove caracteres com encoding irrelevante
def sanitizeWQ(s):
    import ast, re, html
    
    # Remove caracteres unicode irrelevantes (emojis, etc.)
    #r = codecs.charmap_encode(re.sub(r'\\/', '/', s), 'ignore')[0].decode('unicode_escape')
    # r = codecs.charmap_encode(s, 'ignore')[0]#.decode('unicode_escape')
    r = re.sub(r'\\/', '/', s)
    charmap_tuple = codecs.charmap_encode(r, 'ignore')
    u_escaped = charmap_tuple[0].decode('unicode_escape', 'replace')
    
    # Remove surrogate pairs (html emojis (e.g.: '\ud83d\udc4', ' &#55356;&#57117;' ) )
    emojiless_str = re.sub(r'[\uD800-\uDFFF]', '', u_escaped)
    # r = re.sub(r'\\u[0-9a-fA-F]{4}', '', r)
    emojiless_str = re.sub(r'\\u[0-9a-fA-F]{4}', '', emojiless_str)
    # bullet point removal
    # emojiless_str = re.sub(r'&\#[a-zA-Z0-9]{1,5}', '', emojiless_str)
    result = emojiless_str
    result = re.sub(r"[\n\r]", r" ", result)
    
    # undef_chars = result.strip().split()
    # for w in undef_chars:
    #     print(w)
    # print(f'length: {len(undef_chars)}')
    return result

# parses string data from WebQuarto to JSON
def adsDataToJsonWQ(data_str):
    ads = []
    # set loads 'strict' arg to False to allow unescaped characters
    data = json.loads(data_str,strict=False)['ads']
    
    for d in data:
        # Compare and normalize both data shapes
        ad = {
            'url': d['url'], 
            'title': f"{d['title']}",# {d['description']}. {d['about_roommate']}",
            'thumbnail': d['main_photo'],
            'price': d['rent_price'],
            'address': f"{d['address']}, {d['location']}",
            'property_type': f"{d['property_type']}. {d['room_type']}",
            'latlng': f'{d['lat']},{d['lng']}',
            'lat': d['lat'],
            'lng': d['lng'],
            'active': True,
            'modifiedAt': utils.dateTimeNow()
        }
        ads.append(ad)
    return ads


def searchWQ():
    soup = makeSoup(url_wq)
    raw_scripts = soup.find_all("script")
    ads = []
    
    data_str, pagination = findDataWQ(raw_scripts)
    pagination = findPaginationWQ(pagination)
    data_str = sanitizeWQ(data_str)
    ads.append(adsDataToJsonWQ(data_str))
    print(f"WebQuarto Page 1 done")
    
    for i in range(pagination['last_page'] - 1):
        page_url = f"https://www.webquarto.com.br/busca/quartos/recife-pe?page={i + 1}&price_range[]=0,15000&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0"
        makeSoup(page_url)
        raw_scripts = soup.find_all("script")
        data_str, _ = findDataWQ(raw_scripts)
        data_str = sanitizeWQ(data_str)
        ads.append(adsDataToJsonWQ(data_str))
        print(f"WebQuarto Page {i+1} done")
    
    # Dados dos anúncios em flat list
    ads = [item for sublist in ads for item in sublist]
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


async def scrapeAndPrint():
    running = True
    while running:
        curr_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        print(f"\nScraping now... ({curr_time})\n")
        
        # dfWQ = utils.makeDataFrame(searchWQ())
        # dfOLX = utils.makeDataFrame(searchOLX())
        dfOLX = repo.saveAll(searchOLX)
        
        # searchWQ corrections pending
        dfWQ = repo.saveAll(searchWQ)
        
        curr_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        print(f"\nScraping finished ({curr_time})\n")
        
        # concat DFs before saving
        df = pd.concat([dfWQ, dfOLX])
        saveData(df)
        repo
        break
        await asyncio.sleep(3600) # secs

# asyncio.run(scrapeAndPrint())
searchOLX()