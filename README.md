# PTech Django Starter

Template base para iniciar projetos Django da PTech com uma pilha moderna já configurada: Django, Django REST Framework, Jazzmin, Celery, suporte a SQLite/MySQL e o pacote `ptech-tools`.

Este repositório foi pensado para ser usado como **GitHub Template Repository**. A ideia é criar um novo projeto a partir dele, ajustar os nomes do projeto/app quando necessário e começar a desenvolver sem repetir a configuração inicial toda vez.

## O Que Vem Pronto

- Django 6 com estrutura inicial de projeto.
- Django REST Framework configurado.
- Admin com Jazzmin.
- Celery configurado com Redis como broker padrão.
- SQLite por padrão para desenvolvimento local rápido.
- MySQL via variáveis de ambiente.
- `.env` carregado automaticamente sem dependência extra.
- `ptech-tools` instalado e registrado em `INSTALLED_APPS`.
- Comando `export_db` disponível via `python manage.py export_db`.
- Página inicial simples em `/`.
- Endpoint REST de health check em `/api/health/`.
- Testes com `pytest` e `pytest-django`.
- CI básico com GitHub Actions.

## Stack

- Python `>=3.12`
- Django `>=6.0.5,<6.1`
- Django REST Framework `>=3.17.1,<3.18`
- django-jazzmin `>=3.0.4,<3.1`
- Celery `>=5.6.3,<5.7`
- ptech-tools `>=0.1.0,<0.2`
- mysqlclient `>=2.2.8,<2.3`
- pytest e pytest-django para testes

## Estrutura

```text
.
├── app/
│   ├── templates/app/
│   ├── tasks.py
│   ├── urls.py
│   └── views.py
├── core/
│   ├── asgi.py
│   ├── celery.py
│   ├── env.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tests/
├── manage.py
├── pyproject.toml
├── requirements.txt
└── .env.example
```

Papéis principais:

- `core`: projeto Django, com settings, URLs globais, ASGI, WSGI e Celery.
- `app`: primeiro app Django do projeto, com views, URLs, templates e tasks de exemplo.
- `tests`: testes iniciais para API, página inicial, Celery, `.env` e integração com `ptech-tools`.
- `core/env.py`: loader simples de `.env`, sem precisar instalar `python-dotenv`.

## Criando Um Projeto A Partir Do Template

Pela interface do GitHub:

1. Abra este repositório no GitHub.
2. Clique em `Use this template`.
3. Escolha `Create a new repository`.
4. Informe o nome do novo projeto, por exemplo `ptech-zero-problema`.
5. Clone o repositório criado.

Via GitHub CLI:

```bash
gh repo create ptech-zero-problema --template leandrocristovao/ptech-django-starter --public --clone
cd ptech-zero-problema
```

Se o novo projeto for privado, use:

```bash
gh repo create ptech-zero-problema --template leandrocristovao/ptech-django-starter --private --clone
cd ptech-zero-problema
```

## Primeiro Setup Local

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
cp .env.example .env
python -m pip install -r requirements.txt
python -m pip install -e ".[test]"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Depois disso, acesse:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/api/health/`
- `http://127.0.0.1:8000/admin/`

## Variáveis De Ambiente

O arquivo `.env.example` é a base para configuração local. Copie para `.env` e ajuste conforme o projeto.

O arquivo `.env` é carregado automaticamente por `core/settings.py`. Variáveis já exportadas no shell têm prioridade sobre o `.env`.

Principais variáveis:

```env
DJANGO_SETTINGS_MODULE=core.settings
DJANGO_SECRET_KEY=change-me-in-production
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000
DJANGO_LANGUAGE_CODE=pt-br
DJANGO_TIME_ZONE=America/Sao_Paulo
```

## Banco De Dados

Por padrão, o template usa SQLite. Isso permite iniciar um projeto novo sem instalar banco externo.

```env
DJANGO_DATABASE_ENGINE=sqlite
```

Para usar MySQL, ajuste o `.env`:

```env
DJANGO_DATABASE_ENGINE=mysql
MYSQL_DATABASE=ptech_django_starter
MYSQL_USER=root
MYSQL_PASSWORD=secret
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

Depois rode:

```bash
python manage.py migrate
```

## REST API

O Django REST Framework já está em `INSTALLED_APPS` e com configuração inicial em `core/settings.py`.

Endpoint incluído:

```text
GET /api/health/
```

Resposta esperada:

```json
{
  "status": "ok",
  "service": "ptech-django-starter"
}
```

## Admin Com Jazzmin

O Jazzmin já está instalado e vem antes dos apps do Django em `INSTALLED_APPS`, como recomendado para customizar o admin.

Painel:

```text
/admin/
```

Configurações visuais básicas ficam em `JAZZMIN_SETTINGS`, dentro de `core/settings.py`.

## Celery

O Celery está configurado em `core/celery.py`.

Variáveis principais:

```env
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/1
CELERY_TASK_ALWAYS_EAGER=0
CELERY_TASK_EAGER_PROPAGATES=1
```

Para rodar um worker:

```bash
celery -A core worker -l info
```

Existe uma task simples em `app/tasks.py` para validar que a configuração está funcionando.

## PTech Tools

O template já instala `ptech-tools` e registra o app:

```python
INSTALLED_APPS = [
    # ...
    "ptech_tools.apps.PtechToolsConfig",
    "app.apps.AppConfig",
]
```

Com isso, o comando `export_db` já fica disponível:

```bash
python manage.py export_db
```

Exemplo com compressão:

```bash
python manage.py export_db --compress
```

Exemplo filtrando tabelas:

```bash
python manage.py export_db --include-table auth_user --include-table django_session
```

## Testes

Rodar a suíte:

```bash
pytest
```

Ou, se preferir chamar pelo Python da virtualenv:

```bash
python -m pytest
```

Os testes atuais validam:

- endpoint de health check;
- renderização da página inicial;
- task Celery de exemplo;
- loader de `.env`;
- integração com `ptech-tools` e comando `export_db`.

## Build Do Projeto

O projeto possui `pyproject.toml`, então é possível validar build local:

```bash
python -m pip install build
python -m build
```

Isso é útil para confirmar que a estrutura do template está consistente, mesmo que o objetivo principal seja usar este repositório como template.

## Checklist Ao Criar Um Projeto Novo

Depois de criar um repositório a partir deste template, revise:

1. Nome do projeto no `README.md`.
2. `name` e `description` em `pyproject.toml`.
3. `DJANGO_SECRET_KEY` no `.env`.
4. Nome do banco em `MYSQL_DATABASE`, se usar MySQL.
5. `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` para o ambiente real.
6. Nome exibido no admin em `JAZZMIN_SETTINGS`.
7. Conteúdo do app `app`, que é apenas a base inicial.

## Manutenção Do Template

Mudanças feitas neste template valem automaticamente para novos projetos criados depois da alteração.

Projetos já criados a partir do template não recebem atualizações automaticamente. Para esses casos, aplique a mudança manualmente no projeto ou mova a lógica reutilizável para um pacote compartilhado, como `ptech-tools`.

Regra prática:

- código reutilizável entre vários projetos deve ir para `ptech-tools`;
- estrutura inicial, configurações padrão e exemplos devem ficar neste template.
