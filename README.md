# Desafio PFA Docker
Este é um desafio Fullcycle no evento Programa Full Cycle de Aceleração.

## Desafio 1

1. Crie um programa utilizando sua linguagem de programação favorita que faça uma listagem simples do nome de alguns módulos do curso Full Cycle os trazendo de um banco de dados MySQL. Gere a imagem desse container e a publique no DockerHub.
    
    a. container mariadb/mysql https://hub.docker.com/repository/docker/trprado/pfa-db
    
    b. container python https://hub.docker.com/repository/docker/trprado/pfa-app

    c. container nginx https://hub.docker.com/repository/docker/trprado/pfa-nginx

2. Gere uma imagem do nginx que seja capaz que receber as solicitações http e encaminhá-las para o container.
3. Crie um repositório no github com todo o fonte do programa e das imagens geradas.
4. Crie um arquivo README.md especificando quais comandos precisamos executar para que a aplicação funcione recebendo as solicitações na porta 8080 de nosso computador. Lembrando que NÃO utilizaremos Docker-compose nesse desafio.

### Como executar

Criando as imagens
```bash
cd /db
docker build -t dockerhubuser/pfa-db .
cd ../src
docker build -t dockerhubuser/pfa-app .
cd ../nginx
docker build -t dockerhubuser/pfa-nginx .
```

Caso prefira usar a imagem já gerada.
```bash
docker push trprado/pfa-db:v1
docker push trprado/pfa-app:v1
docker push trprado/pfa-nginx:v1
```

Gerando uma rede para comunicação entre containers.
```bash
docker network create pfa
```

Gerando os containers com a rede e executando em segundo plano, onde `dockerhubuser` é seu usuário do dockerhub.io.
```bash
docker run --name pfa-db --rm --net=pfa -d dockerhubuser/pfa-db
docker run --name pfa-app --rm --net=pfa -d dockerhubuser/pfa-app
docker run --name pfa-nginx --rm --net=pfa -p 8080:80 -d dockerhubuser/pfa-nginx
```

Caso tenha usado as imagens do dockerhub, troque `dockerhubuser` por `trprado`.

> Por questão de simplicidade, e como é um desafio, coloquei junto o `.env` usado no app em `/src` e mantive o Dockerfile do banco de dados com as váriaveis de ambiente. Qualquer coisa basta trocar elas já que em nenhum momento existe algo crítico. Mas não é o melhor a se fazer, porém como a imagem deveria ser salva no desafio e permitisse sua execução sem a necessidade de toda uma configuração, essa foi a forma mais simples.

## Desafio 2

Aproveite o desafio 1 que você criou no PFA, a aplicação com sua linguagem favorita, Nginx e MySQL para aplicar o Docker Compose.

Crie o docker-compose.yaml com 3 serviços, um para cada tecnologia. Você deverá configurar os seguintes pontos:

1. O serviço do MySQL não poderá ter um Dockerfile personalizado, é necessário usar diretamente a imagem oficial do MySQL e deverá existir um volume para persistir o banco de dados no projeto, o nome da pasta será dbdata. Deverá usar o entrypoint-initdb.d para já criar um banco e popular dados no banco de dados padrão.

    a. Para resolver isso foi utilizado `volumes` referênciando a pasta **dbdata** para o entrypoint de inicialização de banco de dados `docker-entrypoint-initdb.d`, a pasta **dbdata** foi criada no mesmo nível do **docker-compose.yml**, e contém o arquivo de geração de dados **SQL**.

2. O serviço da sua linguagem favorita deverá continuando a listar dados através da WEB vindo do MySQL. Antes do container iniciar ele deverá verificar se o MySQL já está pronto para conexão, sugerimos usar o Dockerize para fazer esta verificação.

    a. Para resolver esse problema o Dockerfile foi atualizado para instalar junto o Dockerize, porem o CMD de inicialização para de funcionar, caso seja usado o Dockerize pelo arquivo de composição. Então um novo comando foi adicionado, esse comando utiliza o Dockerize para esperar durante 300s pela inicialização do Banco de Dados. A cada 10s o Dockerize verifica se o Banco de Dados esta pronto é executado o script da página web.

3. O serviço do Nginx continuará sendo um proxy reverso para a sua aplicação da linguagem favorita e deverá expor a porta 8000 para acessar a aplicação no browser. Este serviço deverá iniciar somente quando o da sua aplicação da linguagem favorita for iniciado e deverá ser reiniciado automaticamente caso a aplicação da linguagem favorita não esteja rodando ainda.

    a. Para simplificar, não foi mais utilizada o Dockerfile, agora é aberto um volume que interliga o caminho `./nginx/` com `/etc/nginx/conf.d/`, assim o arquivo de configuração fica pronto para o nginx. A porta foi fixada em **8000** como exigido pelo desafio.

4. Os serviços do MySQL e da linguagem favorita devem ter uma rede compartilhada que o Nginx não enxergue e linguagem favorita e Nginx devem ter uma rede compartilhada que o MySQL não enxergue.

    a. Foram criadas três redes, duas apenas internas e uma para comunicação externa.

        1. A rede `network-pfa-db-app` só se comunica entre banco de dados e aplicação, ela é exclusivamente interna.
        2. A rede `network-pfa-app-proxy` só se comunica entre aplicação e a proxy reversa, ela é exclusivamente interna.
        3. A rede `network-proxy` é a única que esta liberada para acesso externo, e ela é usada para acessar o `nginx` na porta **8000**.

Para corrigir seu projeto rodaremos apenas o comando "docker-compose up", tudo já deve ser levantado e estar disponível ao fazer isto, teste bastante isto antes de enviar o desafio para correção.

Divirtam-se e bom trabalho!

### Como Executar

Se for a primeira vez executando, basta fazer:

```
docker-compose up -d
```

Sendo que o `-d` é para desatachar o container da tela.

Caso já tenha criado a imagem da aplicação pelo desafio 1, será necessário executar pela primeira vez de forma diferente:

```bash
docker-compose up --build -d
```
O comando `--build` ira regerar a imagem da aplicação.

Para parar um grupo de containers que estejam no `docker-compose.yml` basta fazer:

```bash
docker-compose stop
```

Para excluir os containers depois de parado ou ao parar excluindo os containers, podemos fazer:

```bash
docker-compose down
```

Uma forma de já excluir a imagem localmente criada é fazer:

```bash
docker-compose down --rmi local
```

Também é possível excluir as demais imagens trocando `local` por `all`.
