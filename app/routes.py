# app/routes.py
from flask import Blueprint, request, jsonify
import datetime
from .models import Task
from .db_session import with_db_session

bp = Blueprint("tasks", __name__)


@bp.route("/", methods=["GET"])
def index_api():
    """
    Route de base du blueprint, indiquant les endpoints disponibles.
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
    Récupère toutes les tâches et les renvoie sous forme de liste JSON.
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
    Renvoie la tâche créée.
    """
    data = request.get_json()
    if not data or not data.get("title") or not data.get("status"):
        return (
            jsonify({"error": "Les champs 'title' et 'status' sont obligatoires."}),
            400,
        )

    due_date = None
    due_date_str = data.get("due_date")
    if due_date_str:
        try:
            due_date = datetime.datetime.fromisoformat(due_date_str)
        except ValueError:
            return (
                jsonify(
                    {
                        "error": "Format de due_date invalide. Utilisez le format ISO (YYYY-MM-DDTHH:MM:SS)."
                    }
                ),
                400,
            )

    new_task = Task(
        title=data.get("title"),
        description=data.get("description"),
        due_date=due_date,
        status=data.get("status"),
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return jsonify(new_task.to_dict()), 201


@bp.route("/tasks/<int:task_id>", methods=["PUT", "PATCH"])
@with_db_session
def update_task(task_id, db):
    """
    Met à jour une tâche existante avec les données fournies.
    Renvoie la tâche mise à jour.
    """
    data = request.get_json()
    task = db.get(Task, task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "status" in data:
        task.status = data["status"]
    if "due_date" in data:
        due_date_str = data.get("due_date")
        if due_date_str:
            try:
                task.due_date = datetime.datetime.fromisoformat(due_date_str)
            except ValueError:
                return (
                    jsonify(
                        {
                            "error": "Format de due_date invalide. Utilisez le format ISO (YYYY-MM-DDTHH:MM:SS)."
                        }
                    ),
                    400,
                )
        else:
            task.due_date = None

    db.commit()
    db.refresh(task)
    return jsonify(task.to_dict()), 200


@bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@with_db_session
def delete_task(task_id, db):
    """
    Supprime la tâche spécifiée par son ID.
    Renvoie un message de confirmation.
    """
    task = db.get(Task, task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    db.delete(task)
    db.commit()
    return jsonify({"message": "Task deleted"}), 200
