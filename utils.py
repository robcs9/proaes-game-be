from bs4 import BeautifulSoup
# from urllib.request import urlopen
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import time
# import requests as rq
# from io import StringIO

url = "https://www.olx.com.br/imoveis/aluguel/estado-pe/grande-recife/recife?pe=2000&ret=1020&ret=1060&ret=1040&sd=3747&sd=3778&sd=3766&sd=3764&sd=3762&o=2"
# headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

from curl_cffi import requests as currq
res = currq.get(url, impersonate="chrome")
soup = BeautifulSoup(res.text, 'lxml')
print(soup.find('script', {"id": "__NEXT_DATA__"}).get_text())


from selenium import webdriver
def makeSeleniumSoup(url):
    driver = webdriver.Firefox()
    driver.get(url)
    content = driver.page_source.encode("utf-8").strip()
    soup = BeautifulSoup(content, "lxml") # alt parser: html.parser
    return soup

# WQ 
# for i, ad in enumerate(ads):
        # print(f'------ begin {i} -----\n{ad}\n------ end {i} -----\n')
        
# for i, ad in enumerate(ads):
        # print(f'------ begin {i} -----\n{ad}\n------ end {i} -----\n')
    
    """ df = pd.DataFrame({
        'active': ads[0]['active'],
        'url': ads[0]['url'],
        'title': ads[0]['title'],
        'description': ads[0]['description'],
        'main_photo': ads[0]['main_photo'],
        'rent_price': ads[0]['rent_price'],
        'address': ads[0]['address'],
        'location': ads[0]['location'],
        'property_type': ads[0]['property_type'],
        'room_type': ads[0]['room_type'],
        'gender': ads[0]['gender'],
        'min_age': ads[0]['min_age'],
        'about_roommate': ads[0]['about_roommate'],
        'lgbt_friendly': ads[0]['lgbt_friendly'],
        'min_age': ads[0]['min_age'],
        'max_age': ads[0]['max_age'],
        'available_at': ads[0]['available_at']
    }) """

    # failed attempt to create a dataframe from a Series:
    # TypeError: int() argument must be a string, a bytes-like object or a real number, not '_NoValueType'
    # p = pd.DataFrame(pd.Series(ads))
    
    # p = pd.Series(ads[0])
    # print(f'\nSingle ad example:\n\n{p}')
    
import asyncio
# asyncio.run(some_fn())

# renaming columns test
# foo = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})

# print(foo)
# foo = foo.rename(columns={"A": "a", "B": "c"})

# print(foo)