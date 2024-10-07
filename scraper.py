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
url_olx = "https://www.olx.com.br/imoveis/aluguel/estado-pe/grande-recife/recife?pe=2000&ret=1020&ret=1060&ret=1040&sd=3747&sd=3778&sd=3766&sd=3764&sd=3762"

# WebQuartos
url = "https://www.webquarto.com.br/busca/quartos/recife-pe/Cordeiro%7CV%C3%A1rzea%7CTorre%7CTorr%C3%B5es%7CMadalena%7CIputinga?price_range%5B%5D=0,2200&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0"

#wq_r = rq.get(url, headers=headers)
#soup1 = BeautifulSoup(wq_r.text, 'lxml')

from selenium import webdriver
import math
def seleniumTest():
    driver = webdriver.Firefox()
    driver.get(url_olx)
    #time.sleep(5)
    content = driver.page_source.encode("utf-8").strip()
    soup = BeautifulSoup(content, "html.parser")
    #driver.quit()
    
    total_results_str = soup.find("div", {"id": "total-of-ads"}).p.get_text().split(" ")[-2]
    pages_count = math.ceil(int(total_results_str) / 50)
    # print(f'pages_count = {pages_count}')
    pages = []
    
    for i in range(1, pages_count + 1):
    # for i in range(1,2):
        page_url = f'{url_olx}&o={i}'
        driver.get(page_url)
        # time.sleep(10)
        content = driver.page_source.encode("utf-8").strip()
        soup = BeautifulSoup(content, "html.parser")
        sections = soup.findAll(class_="olx-ad-card olx-ad-card--horizontal")
        pages.append(sections)
        print(f"Got Page {i}")
        
        import json
        soup1 = BeautifulSoup(content, "lxml")
        data_str = soup1.find("script", {"id": "__NEXT_DATA__"}).get_text()
        data = json.loads(data_str)['props']['pageProps']['ads']
        # attrs:
        # 'title', 'price', 'professionalAd', 'thumbnail', 'url', 'date', 'location',
        # 'municipality', 'neighbourhood', 'uf', 'category'
        print(data[0]['title'])
    
    driver.quit()
    
    # for sections in pages:
        # print(f'sections count: {len(sections)}')
        # print(f'{sections[-1]}')
        #for sect in sections:
            
        #print(pages[0][i])
        #link = pages[0][0].a#['href']
        #ads_data = page.findAll("div", )
        #print(link)
    
    
    # sections = soup.findAll(class_="olx-ad-card olx-ad-card--horizontal")
    
    
    # Data Cleanup
    
    
    # print(sections)

seleniumTest()

# broken due to cloudflare protection
def search_OLX():
    # class = olx-ad-card olx-ad-card--horizontal olx-ad-card--highlight
    html = rq.get("https://olx.com.br", headers=h)
    # time.sleep(20) # sleep for JS full loading
    # html.content encodes proper
    soup = BeautifulSoup(html.content, 'lxml')
    sections = soup.find_all("section")
    #section_search = soup.find_all("section", attrs={"data-ds-component": "DS-AdCard"})
    
    # filters don't work for now
    #filtered = soup.find("section", class_="olx-ad-card")
    
    # html_test = '<div name="somediv">somediv</div><section class="another section">another<section id="1" class="olx-ad-card olx-ad-card--horizontal olx-ad-card--highlight" data-ds-component="DS-AdCard"></section><section class="one more section">more</section>'
    # test = BeautifulSoup(html_test, 'lxml')
    # test_result = test.find("section", class_="more")#.prettify()
    
    # strip().split('<section data-ds-component="DS-AdCard" class="olx-ad-card olx-ad-card--horizontal olx-ad-card--highlight">')
    print(soup)
    result = ""
    # for sect in sections:
    #     print(f'\n\n${sect}\n\n')
        #print("\n------:", sect.find(class_="olx-ad-card"))#.find("a")) #class_=""))
        
    # implement iteration through the many pages (o=1, o=2... o=n) until there are no more pages with olx-ad-cards
    
    #print(result)
# search_OLX()

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
# search_WQ()
