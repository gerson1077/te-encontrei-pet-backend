import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente do processo
load_dotenv()


class Config:
    """Configurações centrais da aplicação Flask, lidas do .env"""

    # Banco de dados (Supabase / PostgreSQL)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Segurança
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    # Ambiente
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

    @staticmethod
    def validar():
        """Verifica se as variáveis essenciais foram carregadas corretamente."""
        obrigatorias = ["DATABASE_URL", "SECRET_KEY", "JWT_SECRET_KEY"]
        faltando = [v for v in obrigatorias if not os.environ.get(v)]
        if faltando:
            raise RuntimeError(
                f"Variáveis de ambiente faltando no .env: {', '.join(faltando)}. "
                "Copie o .env.example para .env e preencha os valores."
            )
