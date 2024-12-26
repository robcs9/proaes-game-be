import asyncio
import repository as repo
import time
from scraper_olx import searchOLX
from utils import validateSavedData
import math

async def main():
    running = True
    while running:
        
        validateSavedData()
        curr_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        begin_timestamp = curr_time

        print(f"\nScraping now... ({curr_time})\n")
        # dfWQ = utils.makeDataFrame(searchWQ())
        # dfOLX = utils.makeDataFrame(searchOLX())
        
        # olx_ads = searchOLX()
        # dfOLX = repo.saveAll(searchOLX)
        repo.saveAll(searchOLX())
        
        # searchWQ corrections pending
        # dfWQ = repo.saveAll(searchWQ)
        
        # curr_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        # print(f"\nScraping finished ({curr_time})\n")
        finish_timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        print(f"\nScraping began at {begin_timestamp} and finished at ({finish_timestamp})\n")
        
        # break
        # Runtime loop
        # await asyncio.sleep(3600) # secs
        # for i in range(3600, 0, -1):
            # print(f"Restarting in {i} secs...")
            # await asyncio.sleep(60)
        for i in range(3600, 0, -60):
            print(f"Restarting in {math.floor(i / 60)} mins...")
            await asyncio.sleep(60)
        
        print('Restarting scraper now!')

# [O.K] - for tests only
# with open('./data/olx_ads_testbase.json') as fd:
#     olx_ads = json.load(fd)['olx_ads']

asyncio.run(main())