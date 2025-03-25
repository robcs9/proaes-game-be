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

DATA_PATH = os.path.join(os.getcwd(), 'data')
DATA_DIR = DATA_PATH if not os.getcwd() == '/root' else '/code/data'

def saveToSupa(geojson: str, f):
  # res = supabase.storage.get_bucket('geojson')
  res = supabase.storage.from_('geojson').upload(
    file=geojson,
    path='./foo.txt',
    file_options={
      "upsert": "true"
    }
  )
  print(res)

# saveToSupa(data, f)
# Testing
print(DATA_DIR)

with open(f'{DATA_DIR}/data.geojson', 'rb') as f:
  # print(type(f.read()))
  # data = json.dumps({'foo': 'bar'})

  res = supabase.storage.from_('geojson').upload(
    file=f.read(),
    path='./data.geojson',
    file_options={
      "content-type": "application/json",
      "upsert": "true"
    }
  )
  print(res)