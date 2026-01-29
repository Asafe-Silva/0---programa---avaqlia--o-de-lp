Registo de Cliques com Data e Hora
==================================
use me:
- Página principal: http://127.0.0.1:5000/
- Painel administrativo: http://127.0.0.1:5000/admin

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

Salvar o arquivo de banco (`database.db`) no Git
-----------------------------------------------

É possível fazer com que o arquivo `database.db` seja adicionado/commitado automaticamente ao repositório Git sempre que houver um novo registro.

Como foi implementado neste projeto:

- O `app.py` inclui duas variáveis de configuração no topo do arquivo:
	- `ENABLE_GIT_COMMIT` (True/False) — quando `True`, o app executa `git add` e `git commit` do arquivo `database.db` depois de cada inserção.
	- `GIT_PUSH` (True/False) — quando `True`, o app tenta também executar `git push` (requer configuração do remoto e credenciais).

Avisos importantes e melhores práticas:

- Commit automático de um arquivo SQLite não é recomendado para colaboração ativa. O arquivo é binário e alterações frequentes podem causar conflitos, histórico grande e problemas de merge.
- Se usar esse recurso, prefira apenas commitar localmente e manter o `push` manual (ou configurar um fluxo seguro de CI/CD).
- Verifique se não há uma entrada em `.gitignore` que impeça `database.db` de ser rastreado. Se houver, remova a linha correspondente.
- Em ambientes multi-usuário, prefira uma base de dados centralizada (Postgres, MySQL, etc.) em vez de compartilhar um arquivo SQLite via Git.

Como ativar (passos rápidos):

1. Abra `app.py` e confirme as variáveis no topo: `ENABLE_GIT_COMMIT = True` e `GIT_PUSH = False`.
2. Garanta que o repositório Git local exista e que `database.db` esteja sendo rastreado (remova entradas em `.gitignore` se necessário):

```powershell
git init
git add database.db
git commit -m "Adicionar database.db ao repositório"
```

3. Se quiser que o app faça `git push` automaticamente, configure `GIT_PUSH = True` e certifique-se de que o repositório remoto esteja configurado e que as credenciais estejam disponíveis no ambiente (ssh key, credential helper, token, etc.).

4. Reinicie a aplicação. A cada clique o app tentará criar um commit com a mensagem automática (caso não haja mudanças relevantes, o commit poderá falhar sem interromper o app).

Autor: Asafe Fagundes Bragança e Silva
-----
Desenvolvido como projeto das disciplinas de ATD e LP.
