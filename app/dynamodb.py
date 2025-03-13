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

def getSession():
  # Load or read dotenv values for AWS access
  env_config = dotenv.dotenv_values('.env')
  aws_config = dict(
    region_name = env_config['AWS_DEFAULT_REGION'],
    aws_access_key_id = env_config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = env_config['AWS_SECRET_ACCESS_KEY'],
  )
  session = boto3.resource('dynamodb', **aws_config)

  return session

