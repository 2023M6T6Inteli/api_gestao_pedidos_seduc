from models.db_credentials import get_engine
from models.entities import Base

from sqlalchemy_utils import (
    database_exists,
    create_database,
    drop_database
)

def main():
    drop_n_create_db()

def drop_n_create_db():
    """
    Drop DB (if existent) and create db schema
    """
    engine = get_engine()
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)
    Base.metadata.create_all(engine)

if (__name__=="__main__"):
    main()