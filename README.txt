Registo de Cliques com Data e Hora
==================================
Descrição
---------
Este projeto é uma aplicação web simples para registar cliques em botões. Cada clique é salvo em uma base de dados SQLite com as seguintes informações:

- `botao`: nome do botão clicado
- `sequencial`: número sequencial do clique (reinicia a cada dia)
- `data`: data do clique (YYYY-MM-DD)
- `hora`: hora do clique (HH:MM)

O front-end inclui um modo escuro (padrão) e um modo claro, e exibe um pequeno cartão com os detalhes do último clique. Há também um painel administrativo para editar, adicionar ou remover botões e exportar os registros.

Estrutura do projeto
--------------------

- `app.py` — aplicação Flask, rotas e lógica da base de dados
- `database.db` — arquivo SQLite (criado automaticamente na raiz do projeto)
- `templates/` — templates Jinja: `index.html`, `admin.html`
- `static/` — arquivos estáticos: `style.css`, `script.js`
- `README.txt` — este ficheiro

Onde fica a base de dados
-------------------------

A base de dados SQLite chama-se `database.db` e fica na raiz do projeto (mesmo nível de `app.py`). O arquivo é criado automaticamente quando a aplicação é executada pela primeira vez, pela função `init_db()` em `app.py`.

Requisitos
----------

- Python 3.8+ (recomendado)
- Flask

Instalação rápida (Windows)
--------------------------

1. Abra o PowerShell na pasta do projeto.
2. (Opcional) crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instale o Flask:

```powershell
pip install flask
```

Como executar
-------------

Na pasta do projeto, execute:

```powershell
python app.py
```

Por padrão a aplicação roda em `host='0.0.0.0'` e `port=5000` (veja o terminal para o endereço exato). Então abra no navegador:

- Página principal: http://127.0.0.1:5000/
- Painel administrativo: http://127.0.0.1:5000/admin

Funcionalidades importantes
--------------------------

- Registro de cliques: cada clique salva nome do botão, número sequencial do dia, data e hora.
- Contador diário: o campo `sequencial` reinicia automaticamente a cada novo dia.
- Painel admin: permite editar nomes de botões, adicionar novos botões, remover botões e baixar os registros em CSV.
- Estatísticas rápidas: a rota `/stats` devolve contagens por botão (hoje e total) e é usada pelo front-end para mostrar badges.
- Exportar: `/admin/export` gera um TXT; `/admin/export_csv` gera CSV com todos os registros.

Notas de implementação
---------------------

- O arquivo `app.py` contém a lógica de criação das tabelas `cliques` e `botoes` (função `init_db`). Se `botoes` estiver vazio, algumas entradas iniciais são inseridas (Botão 1..4).
- O tema (modo escuro/claro) é salvo no `localStorage` do navegador para persistência por usuário.
- Ao remover um botão via admin, os registros antigos desse botão permanecem na tabela `cliques` (não são removidos automaticamente). Se desejar limpar os registros relacionados, é possível estender a rota de remoção para também apagar `cliques` com o mesmo nome.

Segurança e deploy
------------------

- Em ambiente de produção, desative `debug=True` e considere usar um servidor WSGI (uWSGI, Gunicorn) e um proxy reverso (NGINX).
- Para proteger o painel admin pode-se adicionar autenticação (Flask-Login ou outra solução simples).

Problemas comuns
----------------

- Se a aplicação não criar o `database.db`, verifique permissões de escrita na pasta do projeto.
- Se algum botão não aparecer, acesse o painel admin para verificar a tabela `botoes`.

Próximos passos sugeridos
------------------------

- Adicionar paginação e filtros no painel de registros.
- Adicionar autenticação ao painel admin.
- Criar `requirements.txt` com `flask` para facilitar a instalação.

Autor: Asafe Fagundes Bragança e Silva
-----
Desenvolvido como projeto das disciplinas de ATD e LP.
