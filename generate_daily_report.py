#!/usr/bin/env python3
"""
Gera um arquivo JSON com o resumo diário dos cliques para o dia anterior.
Rode este script via Agendador do Windows às 00:01 diariamente.
"""
import sqlite3
import os
import json
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
DATA_DIR = os.path.join(BASE_DIR, 'static', 'data')

os.makedirs(DATA_DIR, exist_ok=True)

# usar o dia anterior
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
# busca botoes
c.execute("SELECT nome FROM botoes ORDER BY id")
botoes = [r[0] for r in c.fetchall()]

summary = {'date': yesterday, 'total': 0, 'counts': []}
for nome in botoes:
    c.execute("SELECT COUNT(*) FROM cliques WHERE botao = ? AND data = ?", (nome, yesterday))
    cnt = c.fetchone()[0]
    summary['counts'].append({'nome': nome, 'count': cnt})
    summary['total'] += cnt

conn.close()

# calcula porcentagens
for item in summary['counts']:
    item['percent'] = round((item['count'] / summary['total'] * 100) if summary['total'] > 0 else 0, 1)

# grava somente se houver pelo menos 1 clique (conforme pedido)
if summary['total'] > 0:
    fname = f"daily_summary_{yesterday}.json"
    path = os.path.join(DATA_DIR, fname)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print('Resumo diário gerado:', path)
else:
    print('Nenhum clique no dia', yesterday, '- nenhum arquivo gerado.')
