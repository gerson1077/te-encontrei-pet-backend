import uuid
from datetime import datetime

from app.extensions import db


class Localizacao(db.Model):
    __tablename__ = "localizacao"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    animal_id = db.Column(db.String(36), db.ForeignKey("animal.id"), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    animal = db.relationship("Animal", backref="localizacoes")

    def to_dict(self):
        return {
            "id": self.id,
            "animal_id": self.animal_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }