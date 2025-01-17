import json, math, re, geoservices
from utils import makeSoup, parseAddress
# Constants
# todo - Rename to URL
url_olx = "https://www.olx.com.br/imoveis/aluguel/estado-pe/grande-recife/recife?pe=1000&ret=1020&ret=1060&ret=1040&sd=3747&sd=3778&sd=3766&sd=3764&sd=3762"

# Retorna a quantidade de páginas de resultados da busca
def findPagePropsOLX(soup):
    data_str = soup.find("script", {"id": "__NEXT_DATA__"}).get_text()
    props = json.loads(data_str)['props']['pageProps']
    return props

# Bottleneck here
# Rework: utilizar o endereço completo, CEP incluso, para melhorar a precisão do geocoding
def getCepOLX(url: str):
    if url is None or url == "" or url.find("olx.com.br") == -1:
        print(f"Improper url provided to getCepOLX. No results found at the url ({url})")
        return
    soup = makeSoup(url)
    script_tag = soup.find('script', string=re.compile(r'(?:dataLayer = )(\[(.*)\])'))
    data_str = ""
    if script_tag is not None:
        data_str = script_tag.get_text(strip=True)
    cep_str = re.search(r'"zipcode":"(\d{8})"', data_str)
    if cep_str is None:
        print(f"Nenhum CEP encontrado na URL: {url}")
        return
    cep = re.search(r'"zipcode":"(\d{8})"', data_str).group(1)
    return cep

def getAddressAdOLX(url: str):
    address = None
    if url is None or url == "" or url.find("olx.com.br") == -1:
        print(f"Improper url provided ({url})")
        return
    soup = makeSoup(url)
    address_tag2 = soup.find('span', string=re.compile(', PE, 5'))
    address_chunk1 = address_tag2.find_previous_sibling().getText(strip=True)
    address_chunk2 = address_tag2.getText(strip=True)
    address = f"{address_chunk1}, {address_chunk2}"
    return address

def extractAdsFromPages(url: str):
    soup = makeSoup(url)
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
            page_url = f'{url}&o={i}'
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
    
    return unfiltereds


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
                'address': addr if addr is not None else ad['location'],
                'property_type': ad['category'],
                'cep': cep if cep is not None else "", # ignore or remove this attr once lat and lng are appended to the dict
            }
            
            try:
                cep_recorded = True if ceps.index(cep) else False
                print(f'Skipping CEP ({cep})' if cep_recorded else '???')
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