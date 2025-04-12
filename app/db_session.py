import functools
import logging
from sqlalchemy.orm import sessionmaker
from .db_engine import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def with_db_session(func):
    """
    Décorateur qui injecte une session de base de données dans la fonction de vue.
    La fonction de vue doit accepter un argument nommé 'db'.
    En cas d'exception, la session est rollbackée et toujours fermée.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        db = SessionLocal()
        try:
            result = func(*args, db=db, **kwargs)
            return result
        except Exception as e:
            db.rollback()
            logging.error(f"Erreur dans la fonction {func.__name__} : {e}")
            raise
        finally:
            db.close()
    return wrapper
