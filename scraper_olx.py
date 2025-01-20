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

def extractAdsFromPages(url: str) -> list[dict]:
    soup = makeSoup(url)
    page_props = findPagePropsOLX(soup)
    pages_count = math.ceil(page_props['totalOfAds'] / page_props['pageSize'])
    
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

def buildAds(unfiltered_ads: list[dict]) -> dict:
    print('Processing raw ad data...')
    unfiltereds_count = len(unfiltered_ads)
    invalid_count = 0
    ads = []
    # addresses = []
    for i, ad in enumerate(unfiltered_ads):
        if ad.get("subject") is None:
            # skip bad results scraped
            invalid_count += 1
            print(f'\nInvalid data (unfiltered) #{i}. Found:\n{ad}')
            # print(f'Found:\n{ad}')
            continue
        
        address = getAddressAdOLX(ad['url'])
        
        ad_data = {
            'url': ad['url'], 
            'title': ad['subject'],
            'price': ad['price'],
            'address': address,
            'property_type': ad['category'],
        }
        # addresses
        ads.append(ad_data)
        print(f"{i+1}/{unfiltereds_count} items have been processed")
    print(f'Invalid ads: {invalid_count}')

def assignGeocodesToAds(geocodes: list[dict], ads: list[dict]):
    print('Assinging geocodes to ads now...')
    notfound_geocoding_count = 0
    for i, ad in enumerate(ads):
        ad['lat'] = geocodes[ad['address']]['lat']
        ad['lng'] = geocodes[ad['address']]['lng']
        
        if ad['lat'] == '' or ad['lng'] == '':
            notfound_geocoding_count += 1
        print(f'{i}/{len(ads)} assigned')
    
    print(f'Not found address geocodings: {notfound_geocoding_count}/{len(ads)}')
    print(f'Total scraped ad links: {len(ads)}')
    print(f'Collected {len(ads)} OLX ads')
    return ads

def searchOLX():
    unfiltereds = extractAdsFromPages(url_olx)
    ads = buildAds(unfiltereds)
    addresses = [ad['address'] for ad in ads]
    geocodes = geoservices.batchGeocodeAddress(addresses)
    
    if geocodes is None:
        raise Exception('Exception: Nenhum resultado encontrado durante o Geocoding dos endereços')
    
    print('Assinging geocodes to ads now...')
    notfound_geocoding_count = 0
    proper_ads = []
    for i, ad in enumerate(ads):
        ad['lat'] = geocodes[ad['address']]['lat']
        ad['lng'] = geocodes[ad['address']]['lng']

        if ad['lat'] == '' or ad['lng'] == '':
            notfound_geocoding_count += 1
        proper_ads.append(ad)
        print(f'{i}/{len(ads)} assigned')
    
    print(f'Not found address geocodings: {notfound_geocoding_count}/{len(ads)}')
    print(f'Total scraped ad links: {len(ads)}')
    print(f'Collected {len(proper_ads)} OLX ads')
    return proper_ads