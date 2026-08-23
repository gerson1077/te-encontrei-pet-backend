from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Instanciadas aqui e inicializadas depois em create_app(),
# para evitar problemas de import circular entre app e models.
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()