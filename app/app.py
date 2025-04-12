from flask import jsonify
from . import create_app

app = create_app()


@app.route("/")
def home():
    return jsonify(
        {
            "message": "Bienvenue sur l'API de gestion de tâches. Utilisez /api/tasks pour accéder aux endpoints."
        }
    )

if __name__ == "__main__":
    app.run()
