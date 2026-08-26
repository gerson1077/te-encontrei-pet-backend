import uuid
from datetime import datetime

from app.extensions import db


class Animal(db.Model):
    __tablename__ = "animal"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)  # "cachorro" ou "gato"
    sexo = db.Column(db.String(10), nullable=True)  # "macho" ou "femea"
    raca = db.Column(db.String(100), nullable=True)
    idade = db.Column(db.Integer, nullable=True)
    foto_url = db.Column(db.String(255), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "especie": self.especie,
            "sexo": self.sexo,
            "raca": self.raca,
            "idade": self.idade,
            "foto_url": self.foto_url,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }
