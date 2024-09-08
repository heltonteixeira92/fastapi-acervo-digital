# fastapi-acervo-digital
Meu Acervo Digital de Romances - Fast Api do Zero (TCC)

![coverage badge](coverage.svg)


### Configurando o ambiente

Para criar o .env copiar de env-sample:

```basg
cp -r contrib/env-sample .env
```

Projeto gerenciado pelo Poetry:

```bash
pip install poetry
```

A versão usada do python é a versão 3.12.4:

```
pyenv local 3.12.4
```

para configurar todo o ambiente basta executar:

```bash
poetry install
```

para ativar o ambiente virtual execute:

```bash
poetry shell
```

#### Comandos

Os comandos para executar funções como suites de testes etc. Estão todas sendo feitas pelo `taskipy`:

###### OBS: Necessário uma instancia de posgresql para rodar localmente.

```bash
task --list
run       Executa o servidor local
lint      Análisa o código e sinaliza erros de estilização
format    Formata a estilização do código seguindo os padrões PEP
test      Executa suite de testes usando Pytest
```

Para executar qualquer comando, basta usar: `task <comando>`

Para criar uma secret key segura:

```bash
import secrets
secrets.token_hex(256)
```

Executando o servidor com docker:

```bash
docker compose build
docker compose up
```