import asyncio
import repository as repo
import time
from scraper_olx import searchOLX
from utils import validateSavedData

async def main():
    running = True
    while running:
        validateSavedData()
        curr_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        print(f"\nScraping now... ({curr_time})\n")
        # dfWQ = utils.makeDataFrame(searchWQ())
        # dfOLX = utils.makeDataFrame(searchOLX())
        
        # olx_ads = searchOLX()
        # dfOLX = repo.saveAll(searchOLX)
        repo.saveAll(searchOLX())
        
        # searchWQ corrections pending
        # dfWQ = repo.saveAll(searchWQ)
        
        curr_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        print(f"\nScraping finished ({curr_time})\n")
        
        break
        # Runtime loop
        # await asyncio.sleep(3600) # secs
        for i in range(3600, 0, -1):
            print(f"Restarting in {i} secs...")
            await asyncio.sleep(1)
        print('Restarting now!')

# [O.K] - for tests only
# with open('./data/olx_ads_testbase.json') as fd:
#     olx_ads = json.load(fd)['olx_ads']

asyncio.run(main())