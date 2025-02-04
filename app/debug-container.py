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

address_tag2 = soup.find('span', string=re.compile(', PE, 5'))
# print(f'address:\n{address_tag2.previous_sibling}')
address_chunk1 = address_tag2.previous_sibling.getText(strip=True)
address_chunk2 = address_tag2.getText(strip=True)
address = f"{address_chunk1}, {address_chunk2}"
print(address)

# getAddressAdOlx replacement logic
# lookup the tag script that has data-json attr if span tags lead nowhere

