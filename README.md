# eventos2

A segunda versão do Sistema de Eventos.

## Desenvolvimento

### Setup

Requisitos:

* [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
  `apt install docker`
* [Docker Compose](https://docs.docker.com/compose/install/)
  `apt install docker-compose`
* [Poetry](https://poetry.eustace.io/docs/)
  `pip install --user --pre poetry`

```sh
# Inicializar o banco de dados
sudo docker-compose up -d

cd backend
# Configurações do backend (editar se necessário)
cp .env.sample .env
# Instalar as dependências do backend
poetry install
# Executar os comandos dentro do virtualenv (criado automaticamente)
poetry run python manage.py migrate
poetry run python manage.py runserver &

cd ../frontend
npm install
npm run serve &
```

Acessar o frontend: http://localhost:8080/

Acessar o backend: http://localhost:8000/api/v1/

**Para fazer um commit, você deve estar dentro do virtualenv do backend.**
Use o poetry para isso:

```
cd backend
poetry shell
cd ..
```

### Teardown

```
# Parar os processos do backend e frontend
kill %1 %2
# Parar o banco de dados
sudo docker-compose down
```
