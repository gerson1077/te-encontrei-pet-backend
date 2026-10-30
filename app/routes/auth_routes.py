import os

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.usuario import Usuario, VALIDADE_TOKEN_MINUTOS

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")
TAMANHO_MINIMO_SENHA = 6


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


@auth_bp.post("/esqueci-senha")
def esqueci_senha():
    """Gera o link de redefinição. O envio de e-mail é SIMULADO: o link sai no console do back-end."""
    dados = request.get_json(silent=True) or {}
    email = (dados.get("email") or "").strip()

    if not email:
        return jsonify({"erro": "Informe o e-mail."}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        token = usuario.gerar_token_reset()
        db.session.commit()
        link = f"{FRONTEND_URL}/redefinir-senha?token={token}"
        print("\n" + "=" * 70)
        print(f"[E-MAIL SIMULADO] Redefinição de senha para {usuario.email}")
        print(f"Link (válido por {VALIDADE_TOKEN_MINUTOS} min): {link}")
        print("=" * 70 + "\n", flush=True)

    # Resposta idêntica exista o e-mail ou não (não revela quais e-mails estão cadastrados)
    return jsonify({
        "mensagem": "Se o e-mail estiver cadastrado, enviamos um link para redefinir a senha."
    }), 200


@auth_bp.post("/redefinir-senha")
def redefinir_senha():
    dados = request.get_json(silent=True) or {}
    token = dados.get("token")
    nova_senha = dados.get("nova_senha")

    if not token or not nova_senha:
        return jsonify({"erro": "Os campos 'token' e 'nova_senha' são obrigatórios."}), 400

    if len(nova_senha) < TAMANHO_MINIMO_SENHA:
        return jsonify({"erro": f"A senha deve ter pelo menos {TAMANHO_MINIMO_SENHA} caracteres."}), 400

    usuario = Usuario.buscar_por_token_reset(token)
    if not usuario:
        return jsonify({"erro": "Link inválido ou expirado. Solicite uma nova redefinição."}), 400

    usuario.set_senha(nova_senha)
    usuario.limpar_token_reset()  # uso único
    db.session.commit()

    return jsonify({"mensagem": "Senha redefinida com sucesso. Faça login com a nova senha."}), 200
