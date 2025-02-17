# Guia de Acomodações para Moradia Estudantil (GAME)

Backend do Guia de Acomodações para Moradia Estudantil (GAME) que possui a finalidade de agregar anúncios de aluguel de moradias e organizá-los com insights relevantes para estudantes e demais interessados em morar no entorno da Cidade Universitária em Recife, Pernambuco.

O scraper é responsável por obter e organizar os dados em formato geojson funciona uma vez a cada hora e necessita de uma chave token da [Geoapify](https://myprojects.geoapify.com) obtível de forma gratuíta.

## Uso

No diretório/pasta do projeto, execute os comandos em um terminal/prompt de comando:

#### Iniciando a aplicação:

```
docker compose up -d --build
```

#### Acessando a aplicação:

No navegador de sua preferência ou cliente de requisições web, acesse o endereço abaixo para visualizar informações sobre a API:
```
http://localhost:8123/docs
```
Ou acesse diretamente o endpoint abaixo para obter os dados geojson:
```
http://localhost:8123/api/v1/geojson
```

#### Parando a aplicação:

```
docker compose stop
```

#### Removendo a aplicação:
```
docker compose down --rmi all -v --remove-orphans
docker image prune
```
Pressione "y" seguido por Enter para confirmar. Depois disso, basta deletar o diretório do projeto.