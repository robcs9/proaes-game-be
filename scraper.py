# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
import requests as rq
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from io import StringIO
import json

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest"
}

# url = "http://www.hubertiming.com/results/2017GPTR10K"
# html = urlopen(url)
# 
# soup = BeautifulSoup(html, 'lxml')
# all_links = soup.find_all("a")
# for link in all_links:
    # print(f'link: ${link}')

# OLX
olx = "https://www.olx.com.br/imoveis/aluguel/estado-pe/grande-recife/recife?pe=2000&ret=1020&ret=1060&ret=1040&sd=3747&sd=3778&sd=3766&sd=3764&sd=3762"

# WebQuartos
url = "https://www.webquarto.com.br/busca/quartos/recife-pe/Cordeiro%7CV%C3%A1rzea%7CTorre%7CTorr%C3%B5es%7CMadalena%7CIputinga?price_range%5B%5D=0,2200&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0"

#wq_r = rq.get(url, headers=headers)
#soup1 = BeautifulSoup(wq_r.text, 'lxml')

def search_WQ():
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    result = soup.find_all("script")

    data_str = ""

    # target between 'window.search' and 'window.search.city_name'
    for line in result:
        content = line.text.strip()
        begin = "window.search = {"
        end = "window.search.city_name"

        if content.find(begin) > -1:
            end_idx = content.find(end)
            data_str = content[len(begin) - 1 : end_idx].strip()[:-1]

    data_json = json.loads(data_str)

    # Dados dos anúncios da busca no WebQuartos
    print(data_json["ads"])
    
search_WQ()