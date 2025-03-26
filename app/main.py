import time, sys, os, dotenv
sys.path.append(os.getcwd())
dotenv.load_dotenv()

import repository as repo
import supabase_utils as supa
from scraper_olx import searchOLX
from dynamodb import saveToAWS
from supabase_utils import saveToSupabase

def main():
    curr_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    begin_timestamp = curr_time
    print(f"\nScraping now... ({curr_time})\n")
    
    data = repo.saveAll(searchOLX())
    
    finish_timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    print(f"\nScraping began at {begin_timestamp} and finished at ({finish_timestamp})\n")

    saveToSupabase()
    return data

if __name__ == "__main__":
    main()