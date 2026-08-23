"""
Script de teste de conexão com o banco Supabase (PostgreSQL)
Rode com: python test_conn.py

Requer: pip install psycopg2-binary python-dotenv
"""

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

database_url = os.environ.get("DATABASE_URL")

if not database_url:
    print("[ERRO] DATABASE_URL não encontrada no .env. "
          "Copie o .env.example para .env e preencha.")
    raise SystemExit(1)

try:
    conn = psycopg2.connect(database_url)
    print("[OK] Conexão com o Supabase estabelecida com sucesso!")
    conn.close()
except Exception as e:
    print("[ERRO] Falha ao conectar no banco:")
    print(e)
