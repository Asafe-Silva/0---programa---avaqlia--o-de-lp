from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = 'database.db'

# Inicializa o banco
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cliques (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            botao TEXT,
            sequencial INTEGER,
            data TEXT,
            hora TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS botoes (
            id INTEGER PRIMARY KEY,
            nome TEXT
        )
    ''')
    # Inicializa botões se não existirem
    c.execute("SELECT COUNT(*) FROM botoes")
    if c.fetchone()[0] == 0:
        botoes_iniciais = [(1, 'Botão 1'), (2, 'Botão 2'), (3, 'Botão 3'), (4, 'Botão 4')]
        c.executemany("INSERT INTO botoes (id, nome) VALUES (?, ?)", botoes_iniciais)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT nome FROM botoes ORDER BY id")
    nomes = [row[0] for row in c.fetchall()]
    conn.close()
    return render_template('index.html', botoes=nomes)

@app.route('/admin')
def admin():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nome FROM botoes ORDER BY id")
    botoes = c.fetchall()
    c.execute("SELECT botao, sequencial, data, hora FROM cliques ORDER BY id DESC LIMIT 50")
    cliques = c.fetchall()
    conn.close()
    return render_template('admin.html', botoes=botoes, cliques=cliques)

@app.route('/admin/update_button', methods=['POST'])
def update_button():
    btn_id = request.json.get('id')
    novo_nome = request.json.get('nome')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE botoes SET nome = ? WHERE id = ?", (novo_nome, btn_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/admin/export')
def export_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, botao, sequencial, data, hora FROM cliques ORDER BY id ASC")
    cliques = c.fetchall()
    conn.close()
    
    output = "ID | Botão | Seq | Data | Hora\n"
    output += "-" * 40 + "\n"
    for cliq in cliques:
        output += f"{cliq[0]} | {cliq[1]} | {cliq[2]} | {cliq[3]} | {cliq[4]}\n"
    
    from flask import Response
    return Response(
        output,
        mimetype="text/plain",
        headers={"Content-disposition": "attachment; filename=registros.txt"}
    )

@app.route('/clicar', methods=['POST'])
def clicar():
    botao = request.json.get('botao')
    agora = datetime.now()
    data_str = agora.strftime('%Y-%m-%d')
    hora_str = agora.strftime('%H:%M')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # pega último clique do dia
    c.execute("SELECT MAX(sequencial) FROM cliques WHERE data = ?", (data_str,))
    last = c.fetchone()[0]
    sequencial = (last or 0) + 1

    # insere no banco
    c.execute(
        "INSERT INTO cliques (botao, sequencial, data, hora) VALUES (?, ?, ?, ?)",
        (botao, sequencial, data_str, hora_str)
    )
    conn.commit()
    conn.close()

    return jsonify({
        'botao': botao,
        'sequencial': sequencial,
        'data': data_str,
        'hora': hora_str
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
