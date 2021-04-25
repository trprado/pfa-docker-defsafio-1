FROM mariadb:10.5

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_USER=pfa
ENV MYSQL_PASSWORD=pfa
ENV MYSQL_DATABASE=pfa-docker

WORKDIR /docker-entrypoint-initdb.d/

COPY ./sql/ .

EXPOSE 3306
