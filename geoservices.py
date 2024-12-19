import os
from time import sleep
import requests
import json
# Loads config altering the env 
# from dotenv import load_dotenv
# load_dotenv()
# print(os.getenv('DOMAIN'))

# Loads config without altering the environment
from dotenv import dotenv_values
config = dotenv_values('.env')
GEOAPIFY_API_KEY = config['GEOAPIFY_API_KEY']

def normalizeCep(cep: str):
    if cep is None or len(cep) < 8 or len(cep) > 9:
        print(f'Falha ao tentar normalizar o CEP ({cep})')
        return
    return f'{cep[:5]}-{cep[5:]}' if cep.find('-') == -1 else cep

# It takes a well-formed CEP (12345-678) as argument
def parseCoords(cep: str):
    cep = normalizeCep(cep)
    api_url = f'https://api.geoapify.com/v1/geocode/search?postcode={cep}&country=brazil&type=postcode&format=json&apiKey={GEOAPIFY_API_KEY}'
    res = requests.get(api_url).json()['results']
    # return { 'lat': res[0]['lat'], 'lon': res[0]['lon'] } if len(res) > 0 else 'Erro: Coordenadas não encontradas - CEP inválido'
    # return f'{res[0]['lat']},{res[0]['lon']}' if len(res) > 0 else 'Erro: Coordenadas não encontradas - CEP inválido'
    return f'{res[0]['lat']},{res[0]['lon']}' if len(res) > 0 else ''
# print(parseCoords('54000-000'))

# Batch request for geocoding of CEPs
def batchGeocode(ceps: list):
    if len(ceps) == 0:
        print('Erro: Nenhum CEP foi passado para ser feito o Geocoding')
        return
    
    normalized_ceps = [] 
    for cep in ceps:
        normalized_ceps.append(normalizeCep(cep))
    
    url = f'https://api.geoapify.com/v1/batch?apiKey={GEOAPIFY_API_KEY}'
    headers = {'Content-Type': 'application/json'}

    inputs = []
    for cep in normalized_ceps:
        inputs.append({"params": {"postcode": cep}})
    
    data = {"api": "/v1/geocode/search","params": {"country": "brazil","type": "postcode", "format": "json"},"inputs":inputs}
    data = json.dumps(data, ensure_ascii=False)
    
    try:
        job_rq = requests.post(url, headers=headers, data=data).json()
        if job_rq.get('error'):
            print(f'Error: {job_rq['message']}')
            return
        job_url = job_rq['url']
        print(f'\nGeocoding Batch requested at {job_url}')
        while True:
            
            job = requests.get(job_url)
            # code 202 -> pending
            if job.status_code == 200:
                job = job.json()
                results = job['results']
                print(f'\nBatch job done. Found {len(results)} CEP results')
                
                coords = []
                # print(results[-1])
                for result in results:
                    r = result['result']['results'] if not result['result'].get('error') else {}
                    lat = ''
                    lng = ''
                    if len(r) > 0:
                        lat = r[0]['lat']
                        lng = r[0]['lon']
                    coords.append({
                        'cep': result['params']['postcode'],
                        'lat': lat,
                        'lng': lng
                    })
                # generator one liner: [r for result in results if len(result['result']['results'] )]
                return coords
            print('\nBatch job ongoing...')
            sleep(10)
    except requests.exceptions.HTTPError as e:
        print(e.response.text)
    # use bias param to improve precision?


# print(batchGeocode(['54330-075','54000-000','55000-000', '111-789']))
# if geocoding with CEP fails, try address search
def toGeocode(addr: str):
    api_url = f'https://api.geoapify.com/v1/geocode/search?text={addr}&filter=countrycode:br&format=json&apiKey={GEOAPIFY_API_KEY}'
    geocode = { 'lat': '', 'lng': ''}
    res = {}
    try:
        # to-do: handle possible json() errors apart
        # e.g.:     raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)
        # requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
        res = requests.get(api_url).json()
    except Exception as e:
        print(f'\nError: {e}')
        print(f'Falha ao tentar geocodificar o endereço: {addr}')
        res['results'] = {}
    if res.get('results') and len(res['results']) > 0:
        res = res['results'][0]
        geocode['lat'] = res['lat']
        geocode['lng'] = res['lon']
    else:
        print('\nAddress text geocoding has failed. No results found\n')
    return geocode


# Debugging
# import json

# ads_path = './data/debug_ads.json'
# coords_path = './data/debug_coords.json'

# with open(ads_path) as fd:
#     ads = json.load(fd)['ads']
# with open(coords_path) as fd:
#     coords = json.load(fd)['coords']

# for ad in ads:
#     for coord in coords:
#         print(f'\ncoord {coord}')
#         print(f'\nad {ad}\n')
#         if coord['cep'] == ad['cep']:
#             ad['lat'] = coord['lat']
#             ad['lng'] = coord['lng']
#             ad.pop('cep')
            