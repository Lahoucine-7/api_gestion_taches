# app/db_init.py
from .db_engine import engine
from .models import Base
import logging


def init_db():
    """
    Initialise la base de données en créant toutes les tables.
    Utilisé lors du démarrage de l'application en développement.
    """
    logging.info("Initialisation de la base de données...")
    Base.metadata.create_all(engine)
    logging.info("Base de données initialisée avec succès.")
