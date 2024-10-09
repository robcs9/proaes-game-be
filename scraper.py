# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
import time
import requests as rq
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from io import StringIO
import json
from selenium import webdriver
import math
import codecs

headers = {
    #"User-Agent": "Mozilla/5.0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "X-Requested-With": "XMLHttpRequest",
    #"Referer": "https://www.olx.com.br/",
}

# OLX req headers
h = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/jxl,image/webp,image/png,image/svg+xml,*/*;q=0.8",
		"Accept-Encoding": "gzip, deflate, br, zstd",
		"Accept-Language": "en-US,en;q=0.5"
		,
		"Connection": "keep-alive",
		"Cookie": "r_id=450519f9-ec6d-4738-8962-38377a678a7c; nl_id=2e281b9d-c8c0-4176-8bbe-caeb41724dab; cf_clearance=jX12rt7F.GFQE56N5zVsQK1D88fPEHcxB0znvr8yaGM-1726229270-1.2.1.1-C2Bu2_tnzT4SFiBtGxLH.KlYgOeSdvbrBMaDhRaY.eV.uOb9_55KFQHOT.iJiyMGZ0KZogjHc5LJT4IhMB88eI2LVBAu_Yv4z5tFJA2Mw6J2S6xCDRu2ntZaDxyzxO.AJsOmd.XXZBL8W2qi7puKg_jsvrbXbe4dw4Wdh1CjspG0rsxNmhjhkO30QYbwjlsDTTTuj_liwkHZVYkhx_PyQVEDPuqGP36RHUmF3dNUONcOUL3DSr4aEwHYpoBIPnCPBJjWNAXRSBZdKxfE.gIFzc8XcRdp2vqTYwtjRhV.JFEYSsAYjiNqOqq_42aJAc_qFJqZwBIbisZQiQAdmXJwTjLL6Ti_fmiMo2qGuLENI6k; _cfuvid=atcWDdPAVKVhp9fN.e0jAZ2qVK640lcD849WlciTszU-1727434007433-0.0.1.1-604800000; TestAB_Groups=txpBdgOrd_entrega.ctafree-ai_on.ppc-myplan-redirect-lp_enabled.ds-header-navbar_enabled.rp-img_enabled.aps-autos-filters-fair_enabled.cmod-security-central-my-ads_control.cnt-rating_v3.trp-cvv-ck_enabled.bjTPZ-aps_enabled.payg-discount-re-julius_ml-ranges.sanityweb50_control.ds-adcard-optimized_on.cnt-scchat_control.prf-authV2_enabled.sxpswgoods_enabled.con-ssr_control.ck-filters_enabled.nv2-modal_enabled.txpNuPay_enabled.adv-li60f8_enabled.autospp-notshow-modal-hv-myads_enabled.autospp-marketplace-header_enabled.payg-discount-julius_ml-c-mab.menu-v1_vrtcal.acrc-reg_control.ck-2-cat_enabled.posfricars_enabled.rp-dup-lnk_enabled.acrc-myacc_control.periodic_12m.fe-bst-gll_control.auto-steps_enabled.must-optin_optin.txtbanrswt_enabled.card-mrp_control.aps-autos-fair-banner_enabled.aps-autos-fair-badge_enabled.nv1-rating_control.auto-placa_enabled.ck-ai-req_enabled.ppf-sub-nc_enabled.sxp-adopt_enabled.adcard-vid_control.acc-phones_enabled.app-bprice_enabled.pass-lvl_enabled.ppffere_control.posautncv2_enabled.ppffernwre_enabled.adv-lifbd3_before.con-optin_A.Autos-foto_enabled.trp-comp_control.poseditrec_diamond.ppfncvch_control.ppffrrnwre_enabled.adv-ho5f03_enabled.crsl-del_control.app-loc_control.swtautnc_enabled.ck-refpric_enabled.semcaptcha_enabled.adv-ad61c2_enabled.fr-shp-ai_enabled.pric-cents_enabled.txpAddCard_control.ai-img-up_control.ck-fipe_enabled.fernwcars_control.hot-ad_enabled.fernwautnc_control; __cf_bm=6hxxcKYrQLnKDFe2e4JYbfxgIKoMXNlWkt_.7srEZ3A-1727434007-1.0.1.1-MlkFRH3qPeiRaupFARLtoyaAIBLD23HomreRjvT6Cekihq5GIkrvygHCiP6BXRQD7.z.dxQAbuYYoZb.mw7BdA",
		"DNT": "1",
		"Host": "www.olx.com.br",
        "If-None-Match": "\"hdxbmgzh61ulzv\"",
		"Priority": "u=0, i",
        "Sec-Fetch-Dest": "document",
		"Sec-Fetch-Mode": "navigate","Sec-Fetch-Site": "cross-site",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
}
HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

# OLX
url_olx = "https://www.olx.com.br/imoveis/aluguel/estado-pe/grande-recife/recife?pe=1000&ret=1020&ret=1060&ret=1040&sd=3747&sd=3778&sd=3766&sd=3764&sd=3762"

# WebQuartos
url_wq = "https://www.webquarto.com.br/busca/quartos/recife-pe/Cordeiro%7CV%C3%A1rzea%7CTorre%7CTorr%C3%B5es%7CMadalena%7CIputinga?price_range%5B%5D=0,1000&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0"

# MGF Imóveis
url_mgf = "https://www.mgfimoveis.com.br/aluguel/quarto/pe-recife-cidade-universitaria?pricemax=1000"

def search_OLX():
    driver = webdriver.Firefox()
    driver.get(url_olx)
    content = driver.page_source.encode("utf-8").strip()
    # soup = BeautifulSoup(content, "html.parser")
    soup = BeautifulSoup(content, "lxml")
    
    # Quantidade de páginas
    script_data = soup.find("script", {"id": "__NEXT_DATA__"}).get_text()
    page_props = json.loads(script_data)['props']['pageProps']
    pages_count = math.ceil(page_props['totalOfAds'] / page_props['pageSize'])
    
    # Calculando quantidade de páginas de resultados da busca
    # total_results = soup.find("div", {"id": "total-of-ads"}).p.get_text().split(" ")[-2]
    # pages_count = math.ceil(int(total_results) / 50)
    # print(f'pages_count = {pages_count}')
    
    # Todos os anúncios extraídos de cada página
    ads = []
    
    for i in range(1, pages_count + 1):
        data = {}
        
        # Evita a repetição do scrape na página inicial
        if i == 1:
            data = page_props['ads']
        else:
            page_url = f'{url_olx}&o={i}'
            driver.get(page_url)
            # time.sleep(10)
            content = driver.page_source.encode("utf-8").strip()
            soup = BeautifulSoup(content, "lxml")
            data_str = soup.find("script", {"id": "__NEXT_DATA__"}).get_text()
            data = json.loads(data_str)['props']['pageProps']['ads']
            
        for d in data:
            # print(f'count: {count}')
            if d.get("subject") is not None:
                ad = {
                   'title': d['subject'],
                   'price': d['price'],
                   'professionalAd': d['professionalAd'],
                   'thumbnail': d['thumbnail'],
                   'url': d['url'],
                   'date': d['date'],
                   'location': d['location'],
                   'category': d['category'],
                }
                ads.append(ad)
        print(f"Page {i} done")
        
    driver.quit()
      
    # Print the data from each ad
    for i, ad in enumerate(ads):
       print(f'\n---- begin ad {i + 1} ----\n{ad}\n---- end ad {i + 1} ----')
    
    print(f'\nTotal ads processed: {len(ads)}')

# seleniumTest()

# WQ test url
url = "https://www.webquarto.com.br/busca/quartos/recife-pe?price_range[]=0,15000&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0"
url_wq = url

# Remove caracteres com encoding irrelevante
def sanitize(str):
    return codecs.charmap_encode(str, 'ignore')

def search_WQ():
    
    html = urlopen(url_wq)
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
    data_str = sanitize(data_str)
    data = json.loads(data_str)['ads']
    
    ads = []
    
    for d in data:
        # ad1 = d.fromkeys(d.keys())
        ad = {
            'active': d['active'],
            'url': d['url'],
            'title': d['title'],
            'description': d['description'],
            'main_photo': d['main_photo'],
            # 'date': d['date'],
            'rent_price': d['rent_price'],
            'address': d['address'],
            'location': d['location'],
            'property_type': d['property_type'],
            'room_type': d['room_type'],
            'gender': d['gender'],
            'min_age': d['min_age'],
            'about_roommate': d['about_roommate'],
            'lgbt_friendly': d['lgbt_friendly'],
            'min_age': d['min_age'],
            'max_age': d['max_age'],
            'available_at': d['available_at']
        }
        ads.append(ad)
    
    # Dados dos anúncios da busca no WebQuartos
    for i, ad in enumerate(ads):
        print(f'------ begin {i} -----\n{ad}\n------ end  {i} -----\n')
search_WQ()