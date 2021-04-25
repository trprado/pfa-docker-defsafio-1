# Desafio PFA Docker
Este é um desafio Fullcycle no evento Programa Full Cycle de Aceleração.

## Desafio 1

1. Crie um programa utilizando sua linguagem de programação favorita que faça uma listagem simples do nome de alguns módulos do curso Full Cycle os trazendo de um banco de dados MySQL. Gere a imagem desse container e a publique no DockerHub.
    
    a. container mariadb/mysql https://hub.docker.com/repository/docker/trprado/pfa-db
    
    b. container python https://hub.docker.com/repository/docker/trprado/pfa-app

2. Gere uma imagem do nginx que seja capaz que receber as solicitações http e encaminhá-las para o container.
3. Crie um repositório no github com todo o fonte do programa e das imagens geradas.
4. Crie um arquivo README.md especificando quais comandos precisamos executar para que a aplicação funcione recebendo as solicitações na porta 8080 de nosso computador. Lembrando que NÃO utilizaremos Docker-compose nesse desafio.

## Como executar

Criando as imagens
```bash
cd /db
docker build -t dockerhubuser/pfa-db .
cd ../src
docker build -t dockerhubuser/pfa-app .
cd ../nginx
docker build -t dockerhubuser/pfa-nginx .
```

Caso prefira usar a imagem já gerada, porém a do nginx ainda é necessário fazer o `build` da imagem.
```bash
docker push trprado/pfa-db:v1
docker push trprado/pfa-app:v1
```

Gerando uma rede para comunicação entre containers.
```bash
docker network create pfa
```

Gerando os containers com a rede e executando em segundo plano, onde `dockerhubuser` é seu usuário do dockerhub.io.
```bash
docker run --name pfa-db --net=pfa -d dockerhubuser/pfa-db
docker run --name pfa-app --net=pfa -d dockerhubuser/pfa-app
docker run --name pfa-nginx --net=pfa -p 8080:80 -d dockerhubuser/pfa-nginx
```

Caso tenha usado as imagens do dockerhub, troque `dockerhubuser` por `trprado`.
