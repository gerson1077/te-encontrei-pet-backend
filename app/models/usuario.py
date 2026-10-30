import hashlib
import secrets
import uuid
from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db

VALIDADE_TOKEN_MINUTOS = 15


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # --- Redefinição de senha: guarda só o HASH do token, nunca o token em si ---
    reset_token_hash = db.Column(db.String(64), nullable=True)
    reset_expira_em = db.Column(db.DateTime, nullable=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def checar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    @staticmethod
    def _hash_token(token):
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def gerar_token_reset(self):
        """Gera um token de uso único (validade curta) e devolve o valor em texto."""
        token = secrets.token_urlsafe(32)
        self.reset_token_hash = self._hash_token(token)
        self.reset_expira_em = datetime.utcnow() + timedelta(minutes=VALIDADE_TOKEN_MINUTOS)
        return token

    def limpar_token_reset(self):
        self.reset_token_hash = None
        self.reset_expira_em = None

    @classmethod
    def buscar_por_token_reset(cls, token):
        """Devolve o usuário dono do token, se ele existir e não tiver expirado."""
        usuario = cls.query.filter_by(reset_token_hash=cls._hash_token(token)).first()
        if not usuario or not usuario.reset_expira_em:
            return None
        if usuario.reset_expira_em < datetime.utcnow():
            return None
        return usuario

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }
