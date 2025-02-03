# Bug: Unable to scrape addresses

import curl_cffi.requests as curlrq
from bs4 import BeautifulSoup
import re

url = 'https://pe.olx.com.br/grande-recife/imoveis/alugo-casa-estilo-kitnet-1355828350'
content = curlrq.get(url, impersonate="chrome")
soup = BeautifulSoup(content.text, "lxml")
# from bs4.diagnose import diagnose
# bad_html = content.text
# diagnose(bad_html)

# print(soup.find('span'))
chnk1 = soup.find('span', string=re.compile(', PE, 5'))
chnk2 = chnk1.find_previous_sibling()
print(chnk2, chnk1)

# lookup the tag script that has data-json attr if span tags lead nowhere
