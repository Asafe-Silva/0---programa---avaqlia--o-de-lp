Registo de Cliques com Data e Hora
==================================

Descrição do Programa
--------------------
Este programa é uma aplicação web simples que permite registar cliques em quatro botões diferentes. 
Cada clique é guardado numa base de dados SQLite com:

- Nome do botão clicado
- Número sequencial do clique (reinicia a cada dia)
- Data do clique
- Hora do clique (horas e minutos)

Além disso, o site possui dois modos de visualização:

1. Modo escuro (padrão) – fundo preto, letras brancas, botões dourados, com vermelho nos hovers.
2. Modo claro – fundo branco, letras pretas, botões dourados, vermelho mais claro nos hovers, amarelo mais escuro.

---

Como Usar
---------

1. Execute o programa:

   - Certifique-se de ter o Python instalado.
   - Instale o Flask com o comando:
     pip install -r requirements.txt
   - Execute o arquivo `app.py`:
     python app.py

2. Abra o navegador e aceda ao endereço indicado no terminal (ex.: http://0.0.0.0:3000 ou http://127.0.0.1:3000).

3. Na página web:
   - Clique em qualquer um dos quatro botões para registar um clique.
   - O número sequencial, data e hora aparecerão imediatamente abaixo dos botões.
   - Para alternar entre modo escuro e claro, clique no botão "Mudar Modo".

4. Cada clique é automaticamente guardado na base de dados `database.db`.

---

Detalhes Técnicos
-----------------
- Front-end: HTML, CSS, JavaScript
- Back-end: Python + Flask
- Base de dados: SQLite
- Contador diário: Reinicia automaticamente a cada novo dia
- Registro persistente: O registo dos cliques mantém-se mesmo após atualizar a página.

---

Notas
-----
- Certifique-se de não apagar o arquivo `database.db` se quiser manter o histórico dos cliques.
- O modo claro e escuro altera apenas a visualização; os dados guardados permanecem iguais.
- É compatível com computadores, tablets e smartphones.

---

Autor
-----
Desenvolvido como projeto das disciplinas de ATD e LP.
