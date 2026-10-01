from flask import Flask
from flask_cors import CORS

from config import Config
from app.extensions import db, migrate, jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Importa os models para o Flask-Migrate detectar as tabelas
    from app.models import animal, localizacao, usuario, termo  # noqa: F401

    # Registra os blueprints (rotas)
    from app.routes.animal_routes import animal_bp
    from app.routes.localizacao_routes import localizacao_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.termo_routes import termo_bp

    app.register_blueprint(animal_bp)
    app.register_blueprint(localizacao_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(termo_bp)

    @app.get("/")
    def health_check():
        return {"status": "ok", "projeto": "Te Encontrei Pet"}

    return app
