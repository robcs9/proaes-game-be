# import sys
# sys.path.append('..')

import repository as repo
import time, os
from scraper_olx import searchOLX
from utils import validateSavedData

def aws():
    import boto3
    db = boto3.resource('dynamodb')
    table = db.Table('geojson')

    print(table.creation_date_time)

def main():
    curr_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    begin_timestamp = curr_time
    print(f"\nScraping now... ({curr_time})\n")
    
    # repo.saveAll(searchOLX())
    data = repo.saveAll(searchOLX())
    
    finish_timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    print(f"\nScraping began at {begin_timestamp} and finished at ({finish_timestamp})\n")

    # Data output
    print(f'Output GeoJSON:\n{data}')
    return data
    
# [O.K] - for tests only
# with open('./data/olx_ads_testbase.json') as fd:
#     olx_ads = json.load(fd)['olx_ads']

if __name__ == "__main__":
    # main()
    aws()