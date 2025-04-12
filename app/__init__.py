from flask import Flask
from .routes import bp as tasks_bp
from .db_init import init_db


def create_app():
    """
    Crée et configure l'application Flask.

    - Active le mode debug.
    - Configure JSON_AS_ASCII pour afficher correctement les accents.
    - Enregistre le blueprint sous le préfixe /api.
    - Initialise la base de données (pour le développement).
    """
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["JSON_AS_ASCII"] = False
    app.register_blueprint(tasks_bp, url_prefix="/api")
    init_db()
    return app
