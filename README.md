# 🗂️ Création d’une API REST de gestion de tâches

## 🧠 Description du Projet
Ce projet consiste à développer une API REST complète pour la gestion des tâches. L'API permet d'effectuer toutes les opérations CRUD (Créer, Lire, Mettre à jour, Supprimer) sur la ressource "Tâche". Elle inclut une validation stricte des données, une gestion rigoureuse des erreurs et des tests unitaires pour assurer sa fiabilité. Le projet est réalisé dans un but d'apprentissage et n'est pas destiné à un usage en production.

## 🎯 Contexte d’Utilisation
Le client est une PME qui souhaite disposer d’un outil interne simple et léger pour organiser et suivre le flux de travail quotidien de ses équipes. L’API doit être sécurisée et facile à intégrer avec d'autres applications internes.

## 📋 Cahier des Charges
- **Objectifs :**
  - Développer une API REST sécurisée avec des endpoints pour toutes les opérations CRUD sur les tâches.
  - Assurer une validation forte des données côté serveur et renvoyer des messages d’erreur clairs.
  - Fournir une documentation complète (README, exemples d'appels, etc.) pour faciliter le déploiement et la maintenance.

- **Livrables :**
  - Un code source complet structuré dans un dépôt Git avec un historique de commits propre.
  - Une documentation détaillée qui inclut le guide d'installation, une description des endpoints et des instructions pour lancer les tests unitaires.

- **Contraintes Techniques :**
  - Réponse aux requêtes CRUD en moins de 200 ms sous une charge modérée.
  - Respect strict des normes PEP8 et des bonnes pratiques de structuration du code.
  - Utilisation de Git avec des commits atomiques et l'adoption de branches pour l'implémentation des fonctionnalités.

## 🛠️ Stack Technologique
- **Langage et Environnement :** Python (version ≥ 3.9) avec gestion d'environnement virtuel (venv ou virtualenv)
- **Framework :** Flask (pour la création de l'API REST)
- **Base de Données :** SQLite (idéal pour le prototypage)
- **ORM :** SQLAlchemy (version 2.x avec typage moderne : Mapped, mapped_column)
- **Tests Unitaires :** Pytest
- **Versionnement :** Git

## ⚙️ Installation et Configuration

### Cloner le dépôt
```bash
git clone <URL_DU_DEPOT>
cd api_gestion_taches
```

### Créer et activer l'environnement virtuel
```bash
python -m venv env
# Sur Windows :
.\env\Scripts\activate
# Sur Linux/Mac :
source env/bin/activate
```

### Installer les dépendances
```bash
pip install -r requirements.txt
```

### Initialiser la base de données
L'initialisation des tables se fait automatiquement au démarrage de l'application.  
Pour forcer l'initialisation manuellement en développement :
```bash
python -m app.db_init
```

## 🚀 Utilisation de l'API

### Démarrer l'application
```bash
python -m app.app
```
L'application sera disponible par défaut à l'adresse :  
`http://127.0.0.1:5000`

### Endpoints Principaux

- **Accueil :**
  - `GET /`  
    Affiche un message de bienvenue et indique l'utilisation de l'API.

- **Index de l'API :**
  - `GET /api/`  
    Renvoie un message indiquant les endpoints disponibles.

- **Liste des Tâches :**
  - `GET /api/tasks`  
    Renvoie la liste de toutes les tâches au format JSON.

- **Détail d'une Tâche :**
  - `GET /api/tasks/<id>`  
    Renvoie les détails d'une tâche spécifique.

- **Création d'une Tâche :**
  - `POST /api/tasks`  
    Payload JSON attendu :
    ```json
    {
      "title": "Nouvelle Tâche",
      "description": "Description de la tâche",
      "due_date": "2025-12-31T00:00:00",
      "status": "pending"
    }
    ```
    Renvoie la tâche créée avec son identifiant.

- **Mise à jour d'une Tâche :**
  - `PUT/PATCH /api/tasks/<id>`  
    Met à jour les champs fournis pour la tâche spécifiée.

- **Suppression d'une Tâche :**
  - `DELETE /api/tasks/<id>`  
    Supprime la tâche et renvoie un message de confirmation.

## 🧪 Exécution des Tests Unitaires

Pour lancer les tests, assurez-vous d'être dans le répertoire racine du projet et exécutez :
```bash
pytest
```
Les tests se trouvent dans le dossier `tests/` et couvrent l'ensemble des opérations CRUD.

## 🔮 Remarques et Évolutions Futures
- Ce projet est un projet personnel réalisé dans un but d'apprentissage et n'est pas destiné à un usage en production.

- **Évolutions possibles :**
  - Ajout d'une authentification pour sécuriser les endpoints.
  - Amélioration de la validation des données (avec des bibliothèques comme Marshmallow ou Pydantic).
  - Documentation interactive avec Swagger/OpenAPI.
  - Containerisation (Docker) pour faciliter le déploiement.

## 📄 Licence
Ce projet est un projet personnel réalisé dans un but d'apprentissage. Il est fictif et n'est pas destiné à un usage en production.
