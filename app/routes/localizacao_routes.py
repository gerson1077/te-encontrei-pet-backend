from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.animal import Animal
from app.models.localizacao import Localizacao

localizacao_bp = Blueprint("localizacao_bp", __name__, url_prefix="/animais")


@localizacao_bp.post("/<string:animal_id>/localizacao")
def cadastrar_localizacao(animal_id):
    animal = Animal.query.get(animal_id)
    if not animal:
        return jsonify({"erro": "Animal não encontrado."}), 404

    dados = request.get_json(silent=True) or {}
    latitude = dados.get("latitude")
    longitude = dados.get("longitude")

    if latitude is None or longitude is None:
        return jsonify({"erro": "Os campos 'latitude' e 'longitude' são obrigatórios."}), 400

    nova_localizacao = Localizacao(
        animal_id=animal_id,
        latitude=latitude,
        longitude=longitude,
    )

    db.session.add(nova_localizacao)
    db.session.commit()

    return jsonify(nova_localizacao.to_dict()), 201


@localizacao_bp.get("/mapa")
def listar_animais_no_mapa():
    # Junta cada animal com sua localização mais recente
    resultado = []
    animais = Animal.query.all()

    for animal in animais:
        if animal.localizacoes:
            ultima_localizacao = sorted(
                animal.localizacoes, key=lambda loc: loc.criado_em, reverse=True
            )[0]
            resultado.append({
                **animal.to_dict(),
                "latitude": ultima_localizacao.latitude,
                "longitude": ultima_localizacao.longitude,
            })

    return jsonify(resultado), 200