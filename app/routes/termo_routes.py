from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.animal import Animal
from app.models.termo import Termo

termo_bp = Blueprint("termo_bp", __name__, url_prefix="/termos")


@termo_bp.post("")
@jwt_required()
def assinar_termo():
    usuario_id = get_jwt_identity()
    dados = request.get_json(silent=True) or {}

    animal_id = dados.get("animal_id")
    aceite = dados.get("aceite")

    if not animal_id or aceite is not True:
        return jsonify({"erro": "É necessário informar 'animal_id' e confirmar o aceite do termo."}), 400

    animal = Animal.query.get(animal_id)
    if not animal:
        return jsonify({"erro": "Animal não encontrado."}), 404

    novo_termo = Termo(
        usuario_id=usuario_id,
        animal_id=animal_id,
        aceite=True,
    )

    db.session.add(novo_termo)
    db.session.commit()

    return jsonify(novo_termo.to_dict()), 201


@termo_bp.get("/animal/<string:animal_id>")
def listar_termos_do_animal(animal_id):
    termos = Termo.query.filter_by(animal_id=animal_id).all()
    return jsonify([t.to_dict() for t in termos]), 200
