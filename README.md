# Guia de Acomodações para Moradia Estudantil (GAME)

Backend do Guia de Acomodações para Moradia Estudantil (GAME) que possui a finalidade de agregar anúncios de aluguel de moradias e organizá-los com insights relevantes para estudantes e demais interessados em morar no entorno da Cidade Universitária em Recife - PE.

## Uso

No diretório/pasta do projeto, execute os comandos em um terminal/prompt de comando:

Iniciando a aplicação:

```
docker compose up -d --build
```

Parando a aplicação:

```
docker compose stop
```
Removendo os recursos criados e alocados pela aplicação:
```
docker compose down --rmi all -v --remove-orphans
docker image prune
```
Pressione "y" seguido por Enter para confirmar.