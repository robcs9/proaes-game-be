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
    if len(cep) > 9 or len(cep) < 8:
        print(f'Error: Falha ao tentar normalizar. CEP inválido ({cep})')
        return ''
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
        print(f'\nGeocoded CEP batch requested at {job_url}')
        while True:
            job = requests.get(job_url)
            if job.status_code == 200:
                job = job.json()
                results = job['results']
                print(f'\nBatch job done. Found {len(results)} results')
                
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
                return coords
            print('\nBatch job ongoing...')
            sleep(1)
    except requests.exceptions.HTTPError as e:
        print(e.response.text)

    # use bias param to improve precision?

print(batchGeocode(['54330-075','54000-000','55000-000', '111-789']))