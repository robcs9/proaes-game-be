# import sys
# sys.path.append('..')

import repository as repo
import time, os
from scraper_olx import searchOLX
from utils import validateSavedData

import boto3
from boto3.dynamodb.conditions import Key, Attr
import dynamodb
def saveToAWS(geojson: dict):
    # db = boto3.resource('dynamodb')
    db = dynamodb.getSession()
    table = db.Table('geojson')
    
    # Replacing previously stored geojson in table
    res = table.update_item(
        Key={ 'type': 'json' },
        UpdateExpression='SET json = :val1',
        ExpressionAttributeValues={ ':val1': geojson }
    )
    print(f'\nUpdate geojson statement response:\n{res}')

    # Listing geojson stored in table
    print('\nScanning for updated geojson')
    res = table.scan()
    print(res['Items'][0]['json'])

def main():
    curr_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    begin_timestamp = curr_time
    print(f"\nScraping now... ({curr_time})\n")
    
    # repo.saveAll(searchOLX())
    data = repo.saveAll(searchOLX())
    
    finish_timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    print(f"\nScraping began at {begin_timestamp} and finished at ({finish_timestamp})\n")

    # Data output
    # print(f'Output GeoJSON:\n{data}')

    saveToAWS(data)
    return data

# [O.K] - for tests only
# with open('./data/olx_ads_testbase.json') as fd:
#     olx_ads = json.load(fd)['olx_ads']

if __name__ == "__main__":
    main()