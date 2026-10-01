import uuid
from datetime import datetime

from app.extensions import db


class Termo(db.Model):
    __tablename__ = "termo"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario_id = db.Column(db.String(36), db.ForeignKey("usuario.id"), nullable=False)
    animal_id = db.Column(db.String(36), db.ForeignKey("animal.id"), nullable=False)
    aceite = db.Column(db.Boolean, default=False, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship("Usuario", backref="termos")
    animal = db.relationship("Animal", backref="termos")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "animal_id": self.animal_id,
            "aceite": self.aceite,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }
