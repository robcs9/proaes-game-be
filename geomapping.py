import os
# from dotenv import load_dotenv
# load_dotenv()
# print(os.getenv('DOMAIN'))

# Load configuration without altering the environment
from dotenv import dotenv_values
config = dotenv_values('.env')

print(config['GOOGLE_'])

def getCoordsFromCep(cep: str):
    
    return {'lat': '1', 'lng': '2'}

