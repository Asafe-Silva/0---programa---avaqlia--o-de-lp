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
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

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
    app.run(host='0.0.0.0', port=3000, debug=True)
