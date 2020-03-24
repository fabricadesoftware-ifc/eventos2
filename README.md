# eventos2

A segunda versão do Sistema de Eventos.

## Setup para desenvolvimento

O sistema é composto por duas partes: o **backend**, construído em Django, implementa a persistência de dados e regras de negócio, e disponibiliza uma API que segue os princípios REST; e o **frontend**, feito com o framework Nuxt.js.

### Backend

Requisitos:

* [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Poetry](https://poetry.eustace.io/docs/)

```sh
# Inicializar o banco de dados
sudo docker-compose up -d

# Configurações (editar se necessário)
cp .env.sample .env
# Instalar as dependências
poetry install
# Executar os comandos dentro do virtualenv (criado automaticamente)
poetry run python manage.py migrate
poetry run python manage.py runserver
```

O backend responde localmente na porta 8000: http://localhost:8000/api/v1/swagger/. Para mais detalhes sobre o seu funcionamento, leia o [README do diretório eventos2](eventos2/README.md).

**Para fazer um commit, você deve estar dentro do virtualenv do backend.**

Use o poetry para isso:
```sh
poetry shell
```

Configure os hooks de commit para executar verificações de código antes de fazer um commit.

```sh
pre-commit install
```

### Frontend

Requisitos:

* [Node.js](https://nodejs.org/)

```sh
# Todas as operações do frontend devem ser feitas a partir deste diretório
cd frontend

# Instalar as dependências
npm install
# Executar em modo de desenvolvimento
npm run dev
```

Em produção, cada evento tem seu próprio domínio, conforme a sua slug, por exemplo:

* micti-xii.eventos2.fabricadesoftware.ifc.edu.br
* sepe2020.eventos2.fabricadesoftware.ifc.edu.br

Durante o desenvolvimento, precisariamos editar o arquivo de sistema `/etc/hosts` para redirecionar o domínio de cada evento criado para o localhost. Para evitar esse trabalho, tendo em mente que geralmente precisamos acessar um só evento durante o desenvolvimento, podemos forçar o frontend a ignorar o domínio carregar sempre o mesmo slug.

A variável de ambiente `EVENTOS2_FRONTEND_FORCE_SLUG` controla o override do evento a ser carregado. Descomente essa linha já presente no arquivo `.env`:

```ini
EVENTOS2_FRONTEND_FORCE_SLUG=test
```

Agora, basta criar um evento com o slug "test" diretamente no backend. Verifique o [README do diretório eventos2](eventos2/README.md) para aprender a operar o Swagger.

O frontend responde localmente na porta 3000: http://localhost:3000/. Para mais detalhes sobre o seu funcionamento, leia o [README do diretório frontend](frontend/README.md).

## Teardown

```
# Parar o banco de dados
sudo docker-compose down
```
