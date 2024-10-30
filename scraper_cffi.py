from curl_cffi import requests as currq
from bs4 import BeautifulSoup

url = "https://www.olx.com.br/imoveis/aluguel/estado-pe/grande-recife/recife?pe=2000&ret=1020&ret=1060&ret=1040&sd=3747&sd=3778&sd=3766&sd=3764&sd=3762&o=2"
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

res = currq.get(url, impersonate="chrome")
soup = BeautifulSoup(res.text, 'lxml')

print(soup)
#print(res.text) #