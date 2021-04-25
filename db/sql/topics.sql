CREATE DATABASE IF NOT EXISTS `pfa-docker`;

USE `pfa-docker`;

CREATE TABLE module (
    id SERIAL,
    name VARCHAR(30) NOT NULL,

    PRIMARY KEY (id)
) ENGINE=INNODB;

CREATE TABLE topics (
    id SERIAL,
    module_id BIGINT UNSIGNED NOT NULL,
    name VARCHAR(80) NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (module_id)
    REFERENCES module(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=INNODB;

INSERT INTO module (name) VALUES('docker');
INSERT INTO topics (module_id, name) VALUES (
    (SELECT id FROM module WHERE name = 'docker'), 
    'introdução');
INSERT INTO topics (module_id, name) VALUES (
    (SELECT id FROM module WHERE name = 'docker'), 
    'hellow world');
INSERT INTO topics (module_id, name) VALUES (
    (SELECT id FROM module WHERE name = 'docker'), 
    'entendendo imagens e dockerhub');

INSERT INTO module (name) VALUES('kubernets');
INSERT INTO topics (module_id, name) VALUES (
    (SELECT id FROM module WHERE name = 'kubernets'), 
    'introdução ao kubernets');
INSERT INTO topics (module_id, name) VALUES (
    (SELECT id FROM module WHERE name = 'kubernets'), 
    'criando aplicações exemplo e imagem');
INSERT INTO topics (module_id, name) VALUES (
    (SELECT id FROM module WHERE name = 'kubernets'), 
    'entendendo o conceito de services');
