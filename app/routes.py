from flask import Blueprint, request, jsonify
import datetime
from .models import Task
from .db_session import with_db_session

bp = Blueprint("tasks", __name__)


def validate_task_data(data: dict, require_title_status: bool = True) -> str | None:
    """
    Valide les données reçues pour créer ou mettre à jour une tâche.

    Args:
        data (dict): Les données JSON reçues dans la requête.
        require_title_status (bool): Indique si 'title' et 'status' doivent être obligatoires.

    Returns:
        str | None: Retourne un message d'erreur si problème, sinon None.
    """
    if not data:
        return "Requête vide ou invalide."
    if require_title_status:
        if not data.get("title") or not data.get("status"):
            return "Les champs 'title' et 'status' sont obligatoires."
    if "due_date" in data and data["due_date"]:
        try:
            datetime.datetime.fromisoformat(data["due_date"])
        except ValueError:
            return "Format de 'due_date' invalide. Utilisez le format ISO (YYYY-MM-DDTHH:MM:SS)."
    return None


@bp.route("/", methods=["GET"])
def index_api():
    """
    Route d'accueil de l'API.
    """
    return (
        jsonify(
            {
                "message": "Bienvenue sur l'API de gestion de tâches. Endpoints disponibles: /api/tasks"
            }
        ),
        200,
    )


@bp.route("/tasks", methods=["GET"])
@with_db_session
def get_tasks(db):
    """
    Récupère toutes les tâches.
    """
    tasks = db.query(Task).all()
    return jsonify([task.to_dict() for task in tasks]), 200


@bp.route("/tasks/<int:task_id>", methods=["GET"])
@with_db_session
def get_task(task_id, db):
    """
    Récupère une tâche spécifique par son ID.
    """
    task = db.get(Task, task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.to_dict()), 200


@bp.route("/tasks", methods=["POST"])
@with_db_session
def create_task(db):
    """
    Crée une nouvelle tâche à partir des données JSON fournies.
    """
    data = request.get_json()
    error = validate_task_data(data)
    if error:
        return jsonify({"error": error}), 400

    due_date = None
    if data.get("due_date"):
        due_date = datetime.datetime.fromisoformat(data["due_date"])

    new_task = Task(
        title=data["title"],
        description=data.get("description"),
        due_date=due_date,
        status=data["status"],
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return jsonify(new_task.to_dict()), 201


@bp.route("/tasks/<int:task_id>", methods=["PUT", "PATCH"])
@with_db_session
def update_task(task_id, db):
    """
    Met à jour une tâche existante avec les données JSON fournies.
    """
    data = request.get_json()
    task = db.get(Task, task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    error = validate_task_data(data, require_title_status=False)
    if error:
        return jsonify({"error": error}), 400

    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "status" in data:
        task.status = data["status"]
    if "due_date" in data:
        if data["due_date"]:
            task.due_date = datetime.datetime.fromisoformat(data["due_date"])
        else:
            task.due_date = None

    db.commit()
    db.refresh(task)
    return jsonify(task.to_dict()), 200


@bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@with_db_session
def delete_task(task_id, db):
    """
    Supprime une tâche spécifique par son ID.
    """
    task = db.get(Task, task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.delete(task)
    db.commit()
    return jsonify({"message": "Task deleted"}), 200
