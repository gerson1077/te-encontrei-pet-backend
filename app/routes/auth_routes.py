from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.usuario import Usuario

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.post("/registrar")
def registrar():
    dados = request.get_json(silent=True) or {}

    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not nome or not email or not senha:
        return jsonify({"erro": "Os campos 'nome', 'email' e 'senha' são obrigatórios."}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"erro": "Já existe um usuário cadastrado com este e-mail."}), 409

    novo_usuario = Usuario(nome=nome, email=email)
    novo_usuario.set_senha(senha)

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify(novo_usuario.to_dict()), 201


@auth_bp.post("/login")
def login():
    dados = request.get_json(silent=True) or {}

    email = dados.get("email")
    senha = dados.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Os campos 'email' e 'senha' são obrigatórios."}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not usuario.checar_senha(senha):
        return jsonify({"erro": "E-mail ou senha inválidos."}), 401

    token = create_access_token(identity=usuario.id)

    return jsonify({
        "access_token": token,
        "usuario": usuario.to_dict(),
    }), 200
