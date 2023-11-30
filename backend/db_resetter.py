import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.db_credentials import get_engine
from models.entities import Base
from sqlalchemy_utils import database_exists, create_database, drop_database

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        drop_n_create_db()
    except Exception as e:
        logger.error("Erro ao executar drop_n_create_db", exc_info=True)

def drop_n_create_db():
    """
    Drop DB (if existent) and create db schema
    """
    try:
        engine = get_engine()
        if database_exists(engine.url):
            logger.info("Banco de dados existe, excluindo...")
            drop_database(engine.url)
        logger.info("Criando banco de dados...")
        create_database(engine.url)
        logger.info("Banco de dados criado com sucesso!")
        logger.info("Criando tabelas...")
        Base.metadata.create_all(engine)
        logger.info("Tabelas criadas com sucesso!")
    except Exception as e:
        logger.error("Erro durante drop_n_create_db", exc_info=True)

if __name__ == "__main__":
    main()
