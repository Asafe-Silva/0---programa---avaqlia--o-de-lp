from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import sqlite3
from datetime import datetime
import subprocess
import os
import shutil

app = Flask(__name__)
DB_PATH = 'database.db'
# Git auto-commit settings
# WARNING: committing a SQLite file into git on every write can cause repository bloat
# and merge conflicts. Use with caution. By default commits are enabled but push is disabled.
ENABLE_GIT_COMMIT = True
GIT_PUSH = False
GIT_REPO_PATH = os.path.dirname(os.path.abspath(__file__))

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
    c.execute("SELECT id, nome FROM botoes ORDER BY id")
    botoes = c.fetchall()
    conn.close()
    return render_template('index.html', botoes=botoes)

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


@app.route('/stats')
def stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nome FROM botoes ORDER BY id")
    botoes = c.fetchall()
    resultado = []
    hoje = datetime.now().strftime('%Y-%m-%d')
    for b in botoes:
        bid, nome = b[0], b[1]
        c.execute("SELECT COUNT(*) FROM cliques WHERE botao = ? AND data = ?", (nome, hoje))
        hoje_qt = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM cliques WHERE botao = ?", (nome,))
        total_qt = c.fetchone()[0]
        resultado.append({'id': bid, 'nome': nome, 'hoje': hoje_qt, 'total': total_qt})
    conn.close()
    return jsonify(resultado)


def get_counts_for_date(date_str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT nome FROM botoes ORDER BY id")
    botoes = [r[0] for r in c.fetchall()]
    resultado = []
    for nome in botoes:
        c.execute("SELECT COUNT(*) FROM cliques WHERE botao = ? AND data = ?", (nome, date_str))
        cnt = c.fetchone()[0]
        resultado.append({'nome': nome, 'count': cnt})
    conn.close()
    return resultado


@app.route('/api/counts_by_date')
def api_counts_by_date():
    date_str = request.args.get('date')
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')
    data = get_counts_for_date(date_str)
    return jsonify({'date': date_str, 'counts': data})


@app.route('/api/percentages')
def api_percentages():
    # If date provided, use that date, otherwise overall totals
    date_str = request.args.get('date')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT nome FROM botoes ORDER BY id")
    botoes = [r[0] for r in c.fetchall()]
    counts = []
    total = 0
    for nome in botoes:
        if date_str:
            c.execute("SELECT COUNT(*) FROM cliques WHERE botao = ? AND data = ?", (nome, date_str))
        else:
            c.execute("SELECT COUNT(*) FROM cliques WHERE botao = ?", (nome,))
        cnt = c.fetchone()[0]
        counts.append({'nome': nome, 'count': cnt})
        total += cnt
    conn.close()
    # calculate percentages
    for item in counts:
        item['percent'] = round((item['count'] / total * 100) if total > 0 else 0, 1)
    return jsonify({'date': date_str, 'total': total, 'data': counts})


@app.route('/api/daily_summary_file')
def api_daily_summary_file():
    # serve pre-generated daily summary JSON if exists in static/data
    date_str = request.args.get('date') or datetime.now().strftime('%Y-%m-%d')
    fname = f"daily_summary_{date_str}.json"
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data')
    file_path = os.path.join(data_dir, fname)
    if os.path.exists(file_path):
        return send_from_directory(data_dir, fname, mimetype='application/json')
    # fallback: compute on the fly
    counts = get_counts_for_date(date_str)
    total = sum([c['count'] for c in counts])
    for c in counts:
        c['percent'] = round((c['count'] / total * 100) if total > 0 else 0, 1)
    return jsonify({'date': date_str, 'total': total, 'counts': counts})


@app.route('/admin/add_button', methods=['POST'])
def add_button():
    nome = request.json.get('nome')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COALESCE(MAX(id),0)+1 FROM botoes")
    new_id = c.fetchone()[0]
    c.execute("INSERT INTO botoes (id, nome) VALUES (?, ?)", (new_id, nome))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'id': new_id, 'nome': nome})


@app.route('/admin/delete_button', methods=['POST'])
def delete_button():
    btn_id = request.json.get('id')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM botoes WHERE id = ?", (btn_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})


@app.route('/admin/export_csv')
def export_csv():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, botao, sequencial, data, hora FROM cliques ORDER BY id ASC")
    cliques = c.fetchall()
    conn.close()
    import csv, io
    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(['ID', 'Botao', 'Sequencial', 'Data', 'Hora'])
    for row in cliques:
        rid, botao, seq, data_db, hora = row
        # format date for export as dd/mm/YYYY
        try:
            parts = data_db.split('-')
            data_fmt = f"{parts[2]}/{parts[1]}/{parts[0]}"
        except Exception:
            data_fmt = data_db
        writer.writerow([rid, botao, seq, data_fmt, hora])
    from flask import Response
    return Response(si.getvalue(), mimetype='text/csv', headers={"Content-disposition": "attachment; filename=registros.csv"})

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
        rid, botao, seq, data_db, hora = cliq
        try:
            p = data_db.split('-')
            data_fmt = f"{p[2]}/{p[1]}/{p[0]}"
        except Exception:
            data_fmt = data_db
        output += f"{rid} | {botao} | {seq} | {data_fmt} | {hora}\n"
    
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
    # store date in DB as ISO (YYYY-MM-DD) for consistent querying
    data_db = agora.strftime('%Y-%m-%d')
    hora_str = agora.strftime('%H:%M')
    # display date in dd/mm/YYYY for UI
    data_display = agora.strftime('%d/%m/%Y')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # pega último clique do dia
    c.execute("SELECT MAX(sequencial) FROM cliques WHERE data = ?", (data_str,))
    last = c.fetchone()[0]
    sequencial = (last or 0) + 1

    # insere no banco
    c.execute(
        "INSERT INTO cliques (botao, sequencial, data, hora) VALUES (?, ?, ?, ?)",
        (botao, sequencial, data_db, hora_str)
    )
    conn.commit()
    conn.close()

    # opcional: commitar o arquivo de banco no repositório git local
    if ENABLE_GIT_COMMIT:
        try:
            git_exe = shutil.which('git') if 'shutil' in globals() else None
        except Exception:
            git_exe = None

        # fallback: assume git is in PATH
        if git_exe is None:
            git_exe = 'git'

        commit_msg = f"Registro: {botao} seq:{sequencial} {data_str} {hora_str}"
        try:
            # git add
            subprocess.run([git_exe, 'add', DB_PATH], cwd=GIT_REPO_PATH, check=False)
            # git commit (allow empty when no changes)
            subprocess.run([git_exe, 'commit', '-m', commit_msg, '--', DB_PATH], cwd=GIT_REPO_PATH, check=False)
            if GIT_PUSH:
                subprocess.run([git_exe, 'push'], cwd=GIT_REPO_PATH, check=False)
        except Exception as e:
            # não interrompe o fluxo; apenas loga
            print('Git auto-commit falhou:', e)

    return jsonify({
        'botao': botao,
        'sequencial': sequencial,
        'data': data_display,
        'hora': hora_str
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
