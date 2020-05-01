# eventos2 - backend

O objetivo do backend é a prover uma API que o frontend possa interagir com os dados do sistema. O backend usa a framework Django com o pacote Django Rest Framework (DRF) para facilitar a construção da API seguindo os princípios REST.

**Leia a documentação dos frameworks, e todo esse documento, antes de começar a desenvolver.**

## API

### Autenticação

A identificação dos clientes ocorre por JSON Web Tokens (JWT). Um token é obtido por meio do endpoint `/token/` e deve ser enviado em cada requisição subsequente, no cabeçalho `Authorization`, prefixado com `Bearer ` (com espaço).

### Documentação

A interface do Swagger localizada em http://localhost:8000/api/v1/swagger/ é usada para explorar a API.

Para usar endpoints que necessitam de autenticação:

1. Utilize o endpoint `/token/` para obter um access token
2. Pressione o botão _Authorize_ no topo da página.
3. Preencha o campo de texto com o token, prefixado com a palavra Bearer, seguida de um espaço. Por exemplo: `Bearer eyJ0eXAiO...`

## Gerenciamento de dependências

Os pacotes necessários para o funcionamento estão especificados no arquivo `pypoetry.toml`. Os requisitos não devem ser alterados manualmente. Em vez disso, o gestor de pacotes [Poetry](https://poetry.eustace.io/docs/) deve ser usado, pois verifica de forma mais rígida os requisitos de versão.

## Configurações

O arquivo de configurações normal do Django é utilizado: `settings.py`. Algumas variáveis, no entando, são parametrizados para aceitar valores de variáveis de ambiente, facilitando a sua modificação em diferentes ambientes (desenvolvimento, produção).

Além das variáveis de ambiente, estes valores são lidos do arquivo `.env`. Um exemplo dos valores que devem ser usados durante o desenvolvimento está no arquivo `.env.sample`.

### Reportagem de erros

Exceções geradas durante a execução do sistema podem ser reportadas para o serviço Sentry por meio da variável de configuração `SENTRY_URL`. Isso é útil principalmente no ambiente de produção.

### Envio de e-mails

_TODO_

### Task queue (tarefas assíncronas)

_TODO_

## Organização do código

### Serializers

A função dos serializers é traduzir objetos JSON enviados pelo cliente para uma representação interna, e vice-versa.

Não é função dos serializers:

* Criar/alterar dados no banco.
* Implementar regras de negócio. Por exemplo: não permitir usuários com e-mail duplicado, utilizando um UniqueValidator.

### Views

A função das views é tratar as requisições dos clientes, retornando uma resposta adequada. Sua principal preocupação é lidar com os métodos e códigos de status do HTTP. Para tal: utiliza os serializers para interpretar os dados de entrada; faz alterações ao banco caso necessário; e utiliza serializers novamente para gerar uma resposta.

As exceções geradas podem ser tratadas na view, ou simplesmente ignoradas, pois o Django Rest Framework sabe como tratá-las. A `NotFoundError`, por exemplo, retornará uma resposta `404 Not Found` automaticamente, caso não for tratada manualmente.

Utilizamos viewsets para agrupar as operações que podem ser feitas sobre cada recurso, abstraindo os métodos HTTP (GET, POST, PUT, DELETE) com actions (retrieve, create, update, destroy).

### URLs / rotas

Tiramos proveito do uso de viewsets, para gerar URLs de forma padronizada, por meio de routers. Cada app define um router, que mapeia as actions de cada viewset registrado para uma URL. Esses routers são adicionados a um roteador global, no arquivo `urls.py`.

### Permissões

Devido aos requisitos do sistema, é necessário fazer o controle de acesso ao nível de objeto. Ou seja, dado usuário pode ter a permissão para modificar certo evento, mas não outro. Para implementar isso, utilizamos o pacote `django-rules`, que permite implementar essa lógica através de `predicates` e `rules`. Leia a documentação desse pacote para entender o funcionamento. 

## Linting

Para identificar e corrigir erros de programação e de formatação, utilizamos as ferramentas `flake8`, `black`, e `bandit`.

## Testing

Para executar os testes, utilizamos o `pytest`:

```sh
poetry run pytest
```

Também pode ser gerado um relatório de coverage no terminal ou em HTML (linha-a-linha).

```sh
poetry run pytest --cov=eventos2
poetry run pytest --cov=eventos2 --cov-report=html --cov-branch
firefox htmlcov/index.html
```
