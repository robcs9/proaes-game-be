# import os
import json
with open("./olxdata.json", "rt", encoding="utf-8") as fd:
    json_str = fd.read()
    data = json.loads(json_str)
    drill = data['props']['pageProps']['ads']  
    # 'title', 'price', 'professionalAd', 'thumbnail', 'url', 'date', 'location',
    # 'municipality', 'neighbourhood', 'uf', 'category'
    print(drill[0]['thumbnail'])
