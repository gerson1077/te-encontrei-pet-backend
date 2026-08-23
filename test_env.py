"""
Script de verificação rápida do .env
Rode com: python test_env.py

Confirma se as variáveis de ambiente essenciais foram carregadas
corretamente antes de tentar rodar as migrations do banco.
"""

import os
from dotenv import load_dotenv

load_dotenv()

variaveis = ["DATABASE_URL", "SECRET_KEY", "JWT_SECRET_KEY"]

print("=== Verificação do .env ===\n")

todas_ok = True
for var in variaveis:
    valor = os.environ.get(var)
    if valor:
        # Mostra só os primeiros caracteres por segurança, nunca a senha inteira
        preview = valor[:15] + "..." if len(valor) > 15 else valor
        print(f"[OK] {var} carregada: {preview}")
    else:
        print(f"[FALTANDO] {var} não encontrada no .env")
        todas_ok = False

print()
if todas_ok:
    print("Tudo certo! As variáveis de ambiente estão configuradas.")
else:
    print("Atenção: copie o .env.example para .env e preencha os valores faltantes.")
