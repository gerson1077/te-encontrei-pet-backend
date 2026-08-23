from flask import Flask

from config import Config
from app.extensions import db, migrate, jwt

from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Libera acesso do front-end (Next.js) ao back-end
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.models import animal  # noqa: F401

    from app.routes.animal_routes import animal_bp
    app.register_blueprint(animal_bp)

    @app.get("/")
    def health_check():
        return {"status": "ok", "projeto": "Te Encontrei Pet"}

    return app