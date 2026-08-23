from dotenv import load_dotenv

# Precisa ser carregado ANTES de importar create_app,
# para garantir que as variáveis de ambiente já estejam disponíveis
# no momento em que o SQLAlchemy tenta se conectar ao banco.
load_dotenv()

from app import create_app  # noqa: E402
from config import Config  # noqa: E402

Config.validar()

app = create_app()

if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
