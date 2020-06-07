# eventos2

A segunda versão do Sistema de Eventos.

## Setup para desenvolvimento

O sistema é composto por duas partes: o **backend**, construído em Django, implementa a persistência de dados e regras de negócio, e disponibiliza uma API que segue os princípios REST; e o **frontend**, feito com o framework Nuxt.js.

Requisitos:

* [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* [Docker Compose](https://docs.docker.com/compose/install/)

```sh
sudo docker-compose up -d
sudo docker-compose exec backend poetry run /tmp/manage.py migrate
sudo docker-compose exec backend poetry run /tmp/manage.py createsuperuser
sudo docker-compose exec backend poetry run /tmp/manage.py populate
```

O frontend poderá ser acessado em https://localhost/, e o backend em https://localhost/api/v1/swagger/. O aviso de certificado inválido pode ser ignorado.

Durante o desenvolvimento, a variável de ambiente `EVENTOS2_FRONTEND_FORCE_SLUG`, já definida com o valor `test` no `docker-compose.yml` controla o override do evento a ser carregado pelo frontend. Em produção, cada evento tem seu próprio domínio, conforme a sua slug.

## Teardown

```
sudo docker-compose down
```
