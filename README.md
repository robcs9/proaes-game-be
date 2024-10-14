# Scraper de Aluguel de Moradias Estudantil

Buscador de anúncios de aluguéis de moradias para estudantes da UFPE.

#### Parâmetros

- Preço máximo: ~ R$ 1000
- Tipo: Quarto, Pensão, República, Apartamento (?), Casa (?)...
- Mobiliado: Sim
- Localidades: Cidade Universitária, Várzea, Engenho do Meio, Jardim São Paulo, Iputinga, Torrões, Cordeiro, Madalena, Torre

### TO-DO

- [x] Corrigir encoding dos caracteres dos dados obtidos na OLX
- [ ] Cruzar informações para tentar encontrar as plataformas/canais de anúncios utilizadas pelos estabelecimentos encontrados no Google Maps

### Estudo:

- [Scraping](https://www.scrapehero.com/web-scraping-with-pandas/)
- [Selenium](https://selenium-python.readthedocs.io/getting-started.html)
- [BeautifulSoup Docs](https://beautiful-soup-4.readthedocs.io/en/latest/)
- [LXML / BeautifulSoup Tutorial](https://www.datacamp.com/tutorial/web-scraping-using-python)

### Fontes:

- [*WebQuarto](https://www.webquarto.com.br/busca/quartos/recife-pe/Cordeiro|V%C3%A1rzea|Torre|Torr%C3%B5es|Madalena|Iputinga?price_range[]=0,2200&has_photo=0&smokers_allowed=0&children_allowed=0&pets_allowed=0&drinks_allowed=0&visitors_allowed=0&couples_allowed=0)

- [*OLX](https://www.olx.com.br/imoveis/aluguel/estado-pe/grande-recife/recife?pe=2000&ret=1020&ret=1060&ret=1040&sd=3747&sd=3778&sd=3766&sd=3764&sd=3762)

- [mgf](https://www.mgfimoveis.com.br/aluguel/quarto/pe-recife-cidade-universitaria)

- [OLX](https://www.olx.com.br/estado-pe?q=aluguel%20quartos&cg=1000)

- [OLX](https://www.olx.com.br/imoveis/aluguel/aluguel-de-quartos/estado-pe?q=aluguel%20quartos)

- [OLX](https://www.olx.com.br/imoveis/aluguel/estado-pe/grande-recife/recife/cidade-universitaria?pe=2000&ret=1020&ret=1060&ret=1040)

- [trovit](https://imoveis.trovit.com.br/alugar-quarto-recife)


### Mapas

- [Moradias Estudantis Recife](https://www.google.com/search?sca_esv=ea85460ec5208a83&tbs=lf:1,lf_ui:2&tbm=lcl&q=moradias+estudantis+recife&rflfq=1&num=10&sa=X&ved=2ahUKEwik5rzu5L-IAxWMq5UCHSdXDRkQjGp6BAgqEAE&biw=1858&bih=972#rlfi=hd:;si:;mv:[[-8.015099137973076,-34.911359265795404],[-8.085044181233394,-34.97736538232835]])

- [República Estudantil Recife](https://www.google.com/search?q=rep%C3%BAblica+estudantil+recife&sca_esv=ea85460ec5208a83&biw=896&bih=971&tbm=lcl&ei=_yfkZpydAqy_1sQPlrKl6A8&oq=republiestudantis+recife&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhhyZXB1YmxpZXN0dWRhbnRpcyByZWNpZmUqAggAMgcQABiABBgNMggQABgHGAgYHjIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBEibYlDdQVjNTnABeACQAQCYAb8BoAH-DKoBBDAuMTC4AQPIAQD4AQGYAgegApAIwgIIEAAYFhgeGA_CAgYQABgeGA_CAggQABgHGB4YD8ICBhAAGAgYHpgDAIgGAZIHAzEuNqAHoDg&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[-8.033457073050673,-34.92552083401562],[-8.068428905050208,-34.95852331247459]])

---

[Abordagem alternativa](https://queroquarto.com/)

---

### Misc

##### OLX:

- Atributos relevantes: 'title', 'price', 'professionalAd', 'thumbnail', 'url', 'date', 'location', 'municipality', 'neighbourhood', 'uf', 'category'
- O atributo "date" pode estar no formato "unix epoch" em alguns casos
