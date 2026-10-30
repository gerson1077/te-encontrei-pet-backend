import uuid
from datetime import datetime

from app.extensions import db

# Valor fixo (simulado) da taxa de colaboração cobrada na adoção
TAXA_COLABORACAO_PADRAO = "30.00"


class Termo(db.Model):
    __tablename__ = "termo"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario_id = db.Column(db.String(36), db.ForeignKey("usuario.id"), nullable=False)
    animal_id = db.Column(db.String(36), db.ForeignKey("animal.id"), nullable=False)
    aceite = db.Column(db.Boolean, default=False, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # --- Prova: pagamento simulado da taxa de colaboração ---
    status_pagamento = db.Column(
        db.String(20), nullable=False, default="pendente", server_default="pendente"
    )
    valor_taxa = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=TAXA_COLABORACAO_PADRAO,
        server_default=TAXA_COLABORACAO_PADRAO,
    )
    pago_em = db.Column(db.DateTime, nullable=True)

    usuario = db.relationship("Usuario", backref="termos")
    animal = db.relationship("Animal", backref="termos")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "animal_id": self.animal_id,
            "aceite": self.aceite,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "status_pagamento": self.status_pagamento,
            "valor_taxa": float(self.valor_taxa) if self.valor_taxa is not None else None,
            "pago_em": self.pago_em.isoformat() if self.pago_em else None,
        }

    def to_dict_com_animal(self):
        dados = self.to_dict()
        a = self.animal
        dados["animal"] = {
            "id": a.id,
            "nome": a.nome,
            "especie": getattr(a, "especie", None),
            "raca": getattr(a, "raca", None),
            "foto_url": getattr(a, "foto_url", None),
        } if a else None
        return dados
