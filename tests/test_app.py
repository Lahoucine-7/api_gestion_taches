# tests/test_app.py
import json
import pytest
import sys
import os

# Ajout du répertoire racine dans sys.path pour accéder au package 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.models import Base
from app.db_engine import engine


@pytest.fixture(scope="module")
def test_client():
    """
    Fixture qui crée un client de test et réinitialise la base de données.
    """
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            Base.metadata.drop_all(bind=engine)
            Base.metadata.create_all(bind=engine)
        yield client
        with app.app_context():
            Base.metadata.drop_all(bind=engine)


def test_get_empty_tasks(test_client):
    response = test_client.get("/api/tasks")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 0


def test_create_task(test_client):
    payload = {
        "title": "Test Task",
        "description": "Ceci est une tâche de test",
        "due_date": "2025-12-31T00:00:00",
        "status": "pending",
    }
    response = test_client.post("/api/tasks", json=payload)
    data = json.loads(response.data)
    assert response.status_code == 201
    assert "id" in data
    assert data["title"] == payload["title"]


def test_get_task(test_client):
    payload = {
        "title": "Get Task",
        "description": "Tâche à récupérer",
        "due_date": "2025-12-31T00:00:00",
        "status": "pending",
    }
    create_resp = test_client.post("/api/tasks", json=payload)
    created_data = json.loads(create_resp.data)
    task_id = created_data["id"]

    response = test_client.get(f"/api/tasks/{task_id}")
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["id"] == task_id


def test_update_task(test_client):
    payload = {
        "title": "Tâche à mettre à jour",
        "description": "Avant mise à jour",
        "due_date": "2025-12-31T00:00:00",
        "status": "pending",
    }
    create_resp = test_client.post("/api/tasks", json=payload)
    created_data = json.loads(create_resp.data)
    task_id = created_data["id"]

    update_payload = {
        "title": "Tâche mise à jour",
        "description": "Après mise à jour",
        "status": "completed",
    }
    update_resp = test_client.put(f"/api/tasks/{task_id}", json=update_payload)
    updated_data = json.loads(update_resp.data)
    assert update_resp.status_code == 200
    assert updated_data["title"] == update_payload["title"]
    assert updated_data["description"] == update_payload["description"]
    assert updated_data["status"] == update_payload["status"]


def test_delete_task(test_client):
    payload = {
        "title": "Tâche à supprimer",
        "description": "Cette tâche sera supprimée",
        "due_date": "2025-12-31T00:00:00",
        "status": "pending",
    }
    create_resp = test_client.post("/api/tasks", json=payload)
    created_data = json.loads(create_resp.data)
    task_id = created_data["id"]

    delete_resp = test_client.delete(f"/api/tasks/{task_id}")
    delete_data = json.loads(delete_resp.data)
    assert delete_resp.status_code == 200
    assert delete_data.get("message") == "Task deleted"

    get_resp = test_client.get(f"/api/tasks/{task_id}")
    assert get_resp.status_code == 404
