from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.animal import Animal

animal_bp = Blueprint("animal_bp", __name__, url_prefix="/animais")


@animal_bp.post("")
def cadastrar_animal():
    dados = request.get_json(silent=True) or {}

    nome = dados.get("nome")
    especie = dados.get("especie")

    if not nome or not especie:
        return jsonify({"erro": "Os campos 'nome' e 'especie' são obrigatórios."}), 400

    novo_animal = Animal(
        nome=nome,
        especie=especie,
        raca=dados.get("raca"),
        idade=dados.get("idade"),
        foto_url=dados.get("foto_url"),
    )

    db.session.add(novo_animal)
    db.session.commit()

    return jsonify(novo_animal.to_dict()), 201


@animal_bp.get("")
def listar_animais():
    animais = Animal.query.order_by(Animal.criado_em.desc()).all()
    return jsonify([a.to_dict() for a in animais]), 200


@animal_bp.get("/<string:animal_id>")
def obter_animal(animal_id):
    animal = Animal.query.get(animal_id)
    if not animal:
        return jsonify({"erro": "Animal não encontrado."}), 404
    return jsonify(animal.to_dict()), 200