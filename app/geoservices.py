import os, requests, json
from time import sleep
from dotenv import dotenv_values, load_dotenv

# Loads config altering the env 
# load_dotenv()
# print(os.getenv('DOMAIN'))

# Loads config without altering the environment
# to-do: use env variable for the file path
# config = dotenv_values('./app/.env') # uncomment this line when running locally
config = dotenv_values('/run/secrets/env_secrets') # uncomment this line when running in containers
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

def batchGeocodeAddress(addresses: list[dict]):
    geocodes = {}
    
    if len(addresses) == 0:
        print('Erro: Nenhum Endereço informado para requisição de Geocode')
        return
    
    url = f'https://api.geoapify.com/v1/batch/geocode/search?apiKey={GEOAPIFY_API_KEY}&format=json'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    # add bias params if extra precision is needed
    try:
        job_url = ''

        TESTING = False
        if TESTING:
            # Performing test with batch request already done to prevent overspending API credits
            GEOCODE_BATCH_TEST_URL = config['GEOCODE_BATCH_TEST_URL']
            print('\n-------------------------------------------------------------------------------------------------------')
            print('This is a test run reusing a previously batch geocode request. Change the flag "TESTING" to turn it off')
            print('-------------------------------------------------------------------------------------------------------\n')
            # job_rq = requests.get(GEOCODE_BATCH_TEST_URL)
            job_url = GEOCODE_BATCH_TEST_URL
            
        else:
            job_rq = requests.post(url, headers=headers, json=addresses).json()
            if job_rq.get('error'):
                print(f'Erro durante a resolução do job request: {job_rq['message']}')
                return
            job_url = job_rq['url']
            print(f'\nGeocoding Batch requested at {job_url}')
        
        while requests.get(job_url).status_code == 202: # pending
            print('\nBatch job ongoing...')
            sleep(1)

        job = requests.get(job_url)
        if job.status_code == 200:
            results = job.json()
            print(f'\nBatch job done. Geocoded addresses: {len(results)}')
            
            for result in results:
                if result.get('place_id') is None:
                    print(f'\nFailed to geocode an adresss from the batch\nError: {result['result']['error']}')
                    result['lat'] = ''
                    result['lng'] = ''
                
                geocodes[result['query']['text']] = {
                    'lat': result['lat'],
                    'lng': result['lon']
                }
            print('Geocode assigments finished')
    except Exception as e:
        # to-do: return geocodes as None instead of an empty dict?
        print(f'Falha durante o processo de batch requests. Erro:\n{e}')
    return geocodes

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