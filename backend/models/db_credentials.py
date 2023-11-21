from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = "root"
DB_PWD = "1234"
DB_HOST = "localhost"
DB_NAME = "academic_db"
DB_DEBUG_MODE = False

def get_engine(db_user=DB_USER, db_pwd=DB_PWD, db_host=DB_HOST, db_name=DB_NAME, db_debug_mode=DB_DEBUG_MODE):
    return create_engine(f"mysql://{db_user}:{db_pwd}@{db_host}/{db_name}", echo=DB_DEBUG_MODE)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    #SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session()