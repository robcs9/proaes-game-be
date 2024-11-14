import os
import requests
# Loads config altering the env 
# from dotenv import load_dotenv
# load_dotenv()
# print(os.getenv('DOMAIN'))

# Loads config without altering the environment
from dotenv import dotenv_values
config = dotenv_values('.env')

def normalizeCep(cep: str):
    if len(cep) > 9 or len(cep) < 8:
        print('Error: Falha ao tentar normalizar - CEP inválido')
        return ''
    return f'{cep[:5]}-{cep[5:]}' if cep.find('-') == -1 else cep

# It takes a well-formed CEP (12345-678) as argument
def parseCoords(cep: str):
    cep = normalizeCep(cep)
    GEOAPIFY_API_KEY = config['GEOAPIFY_API_KEY']
    api_url = f'https://api.geoapify.com/v1/geocode/search?postcode={cep}&country=brazil&type=postcode&format=json&apiKey={GEOAPIFY_API_KEY}'
    res = requests.get(api_url).json()['results']
    # return { 'lat': res[0]['lat'], 'lon': res[0]['lon'] } if len(res) > 0 else 'Erro: Coordenadas não encontradas - CEP inválido'
    # return f'{res[0]['lat']},{res[0]['lon']}' if len(res) > 0 else 'Erro: Coordenadas não encontradas - CEP inválido'
    return f'{res[0]['lat']},{res[0]['lon']}' if len(res) > 0 else ''
# print(parseCoords('54000-000'))

# todo: Batch request for coords parsing