import dotenv, boto3

"""from botocore.config import Config
  my_config = Config(
  region_name = 'sa-east-1',
  # retries = {
  #     'max_attempts': 10,
  #     'mode': 'standard'
  # }
)
client = boto3.client('dynamodb', config=aws_config) """

# Initialize client connection
def init():
  # Load or read dotenv values for AWS access
  env_config = dotenv.dotenv_values('.env')
  aws_config = dict(
    region_name = env_config['AWS_DEFAULT_REGION'],
    aws_access_key_id = env_config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = env_config['AWS_SECRET_ACCESS_KEY'],
  )
  session = boto3.resource('dynamodb', **aws_config)

  return session

def saveToAWS(geojson: dict):
  db = init()
  table = db.Table('geojson')
  
  # Replacing previously stored geojson in table
  res = table.update_item(
      Key={ 'type': 'json' },
      UpdateExpression='SET json = :val1',
      ExpressionAttributeValues={ ':val1': geojson }
  )
  print(f'\ngeojson update statement response:\n{res}')

def getGeojson():
  db = init()
  geojson = None
  try:
    table = db.Table('geojson')
    res = table.scan()
    items = res['Items']
    if len(items) > 0:
      geojson = items[0]['json']
    return geojson
  except Exception as e:
    print(f'Failed to retrieve geojson data from the dynamodb database\n{e}')
    return