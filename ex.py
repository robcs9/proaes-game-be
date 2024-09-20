import pandas as pd
import requests as rq
from io import StringIO

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest"
}

# Alvos de busca: Pensões, Repúblicas, Apto imobiliados, Quartos, Pensionatos

url_webq0 = "https://www.webquarto.com.br/busca/quartos/recife-pe/Cordeiro|V%C3%A1rzea|Torre|Torr%C3%B5es|Madalena|Iputinga?price_rangxe[]=0,2200&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0"

url_webq1 = "https://www.webquarto.com.br/busca/pensionatos/recife-pe?price_range[]=0,15000&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0"

url_webq2 = "https://www.webquarto.com.br/busca/republicas/recife-pe?price_range[]=0,15000&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0"

# Apto
url_zap = "https://zapimoveis.com.br/aluguel"
url_zap_filtro = "https://www.zapimoveis.com.br/aluguel/apartamentos/pe+recife++cid-universitaria/\
            mobiliado/?__ab=sup-hl-pl:newC,exp-aa-test:B,super-high:new,olx:control,\
            phone-page:new,off-no-hl:new,hel-bar:control&transacao=aluguel&onde=,\
            Pernambuco,Recife,,Cidade%20Universit%C3%A1ria,,,neighborhood,\
            BR%3EPernambuco%3ENULL%3ERecife%3EBarrios%3ECidade%20Universitaria,\
            -8.036713,-34.93527,;,Pernambuco,Recife,,V%C3%A1rzea,,,neighborhood,\
            BR%3EPernambuco%3ENULL%3ERecife%3EBarrios%3EVarzea,-8.0484,-34.95909,;,\
            Pernambuco,Recife,,Engenho%20do%20Meio,,,neighborhood,BR%3EPernambuco%3E\
            NULL%3ERecife%3EBarrios%3EEngenho%20do%20Meio,-8.056542,-34.943772,;,\
            Pernambuco,Recife,,Torr%C3%B5es,,,neighborhood,BR%3EPernambuco%3ENULL%3E\
            Recife%3EBarrios%3ETorroes,-8.059463,-34.935972,;,Pernambuco,Recife,,\
            Jardim%20S%C3%A3o%20Paulo,,,neighborhood,BR%3EPernambuco%3ENULL%3ERecife\
            %3EBarrios%3EJardim%20Sao%20Paulo,-8.079947,-34.942802,;,Pernambuco,Recife\
            ,,Iputinga,,,neighborhood,BR%3EPernambuco%3ENULL%3ERecife%3EBarrios%3E\
            Iputinga,-8.047936,-34.925821,&tipos=apartamento_residencial,\
            studio_residencial,kitnet_residencial,casa_residencial,sobrado_residencial\
            ,condominio_residencial,flat_residencial,loft_residencial&pagina=1&\
            amenities=Mobiliado&ordem=Menor%20pre%C3%A7o"
url_olx = "https://www.olx.com.br/estado-pe?q=aluguel&cg=1000"

# requests
url_test = "https://www.amazon.com/Apple-iPhone-Fully-Unlocked-128/dp/B07P611Q4N"
response = rq.get(url_test, headers=headers)
#print(response._content)

# pandas - for tabular data handling
#data = pd.read_html(response.text)
#print(pd.read_html("http://google.com"))
print(pd.read_html(response.text))

# LXML / BeautifulSoup - non-tabular data scraping