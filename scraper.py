import pandas as pd
from bs4 import BeautifulSoup
import json
import math
import codecs
from curl_cffi import requests as curlrq
import time
import asyncio

url_olx = "https://www.olx.com.br/imoveis/aluguel/estado-pe/grande-recife/recife?pe=1000&ret=1020&ret=1060&ret=1040&sd=3747&sd=3778&sd=3766&sd=3764&sd=3762"
url_wq = "https://www.webquarto.com.br/busca/quartos/recife-pe/Cordeiro%7CV%C3%A1rzea%7CTorre%7CTorr%C3%B5es%7CMadalena%7CIputinga?price_range%5B%5D=0,1000&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0"
url_mgf = "https://www.mgfimoveis.com.br/aluguel/quarto/pe-recife-cidade-universitaria?pricemax=1000"


def makeSoup(url):
    content = curlrq.get(url, impersonate="chrome")
    soup = BeautifulSoup(content.text, "lxml")
    return soup

# Retorna a quantidade de páginas de resultados da busca
def findPagePropsOLX(soup):
    data_str = soup.find("script", {"id": "__NEXT_DATA__"}).get_text()
    props = json.loads(data_str)['props']['pageProps']
    return props
    
def searchOLX():
    soup = makeSoup(url_olx)
    page_props = findPagePropsOLX(soup)
    pages_count = math.ceil(page_props['totalOfAds'] / page_props['pageSize'])
    
    ads = []
    
    for i in range(1, pages_count + 1):
        data = {}
        
        # Evita a repetição do scrape na página inicial
        if i == 1:
            data = page_props['ads']
        else:
            page_url = f'{url_olx}&o={i}'
            soup = makeSoup(page_url)
            page_props = findPagePropsOLX(soup)
            data = page_props['ads']

        for d in data:
            if d.get("subject") is not None:
                ad = {
                    'url': d['url'], 
                    'title': d['subject'],
                    'thumbnail': d['thumbnail'],
                    'price': d['price'],
                    'address': d['location'],
                    'property_type': d['category'],
                }
                ads.append(ad)
        print(f"OLX Page {i} done")
        
    return ads


# WQ multi-pages test url
# testing-only, keep commented out otherwise
# url_wq = "https://www.webquarto.com.br/busca/quartos/recife-pe?page=1&price_range[]=0,15000&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0"


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
    
    """ undef_chars = result.strip().split()
    for w in undef_chars:
        print(w) """
    # print(f'length: {len(undef_chars)}')
    return result

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
    print(f"WebQuartos Page 1 done")
    
    for i in range(pagination['last_page'] - 1):
        page_url = f"https://www.webquarto.com.br/busca/quartos/recife-pe?page={i + 1}&price_range[]=0,15000&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0"
        makeSoup(page_url)
        raw_scripts = soup.find_all("script")
        data_str, _ = findDataWQ(raw_scripts)
        data_str = sanitizeWQ(data_str)
        ads.append(adsDataToJsonWQ(data_str))
        print(f"WebQuartos Page {i+1} done")
    
    # Dados dos anúncios em flat list
    ads = [item for sublist in ads for item in sublist]
    return ads

def saveToCSV(df: pd.DataFrame):
    df = df.rename(columns={
        'title': 'Título','thumbnail': 'Foto','price': 'Preço','address': 'Endereço','property_type': 'TipoMoradia'
    })
    df.to_csv("data/data.csv")
    # print(df)
    
def makeDataFrame(data_arr: list, src: str):
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

async def scrapeAndPrint():
    running = True
    while running:
        curtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        print(f"\nScraping now... ({curtime})\n")
        
        dfWQ = makeDataFrame(searchWQ(), "WebQuartos")
        dfOLX = makeDataFrame(searchOLX(), "OLX")
        
        
        curtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        print(f"\nScraping finished ({curtime})\n")
        
        # concat DFs before saving
        df = pd.concat([dfWQ, dfOLX])
        saveToCSV(df)
        break
        await asyncio.sleep(60)

asyncio.run(scrapeAndPrint())

# renaming columns test
""" foo = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

# print(foo)
foo = foo.rename(columns={"A": "a", "B": "c"})

print(foo) """