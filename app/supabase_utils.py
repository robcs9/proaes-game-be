import dotenv, os, json
from supabase import create_client, Client
from supabase.client import ClientOptions

dotenv.load_dotenv('.env')
supabase_url: str = os.getenv('SUPABASE_URL')
supabase_key: str = os.getenv('SUPABASE_PRIVATE_KEY')
supabase: Client = create_client(
  supabase_url,
  supabase_key,
  options=ClientOptions(
    postgrest_client_timeout=10,
    storage_client_timeout=10,
    # schema='geojson'
  )
)

def getGeojson():
  print('Retrieving data.geojson from the Supabase bucket')
  res = supabase.storage.from_('geojson').download('data.geojson')
  try:
    geojson: dict = json.loads(res)
    print('data.geojson has been retrieved successfully from the supabase bucket')
    return geojson
  except Exception as e:
    print(f'Error retrieving data.geojson from the supabase bucket\n{e}')
    return

def saveToSupabase(geojson: dict = None):
  DATA_PATH = os.path.join(os.getcwd(), 'data')
  DATA_DIR = DATA_PATH if not os.getcwd() == '/root' else '/code/data'
  file_location = f'{DATA_DIR}/data.geojson'
  if not os.path.exists(file_location):
    print(f'Failed to find the geojson file at {file_location}')
    return

  print('Uploading data.geojson to the Supabase bucket')
  with open(file_location, 'rb') as f:
    res = supabase.storage.from_('geojson').upload(
      file=f.read(),
      path='./data.geojson',
      file_options={
        "content-type": "application/json",
        "upsert": "true"
      }
    )
    print('data.geojson upload has finished')