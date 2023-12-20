from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv() 

DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_DEBUG_MODE = False

def get_engine(db_user=DB_USER, db_pwd=DB_PWD, db_host=DB_HOST, db_name=DB_NAME, db_debug_mode=DB_DEBUG_MODE):
    # conn_str = f"mysql://{db_user}:{db_pwd}@{db_host}/{db_name}"
    conn_str = f"mysql+mysqlconnector://{db_user}:{db_pwd}@{db_host}/{db_name}"
    print(conn_str)
    
#     return create_engine(conn_str, echo=DB_DEBUG_MODE)

def get_engine():
    conn_str = "postgresql://postgres:senha123@database-2.c86pb1hq4aoj.us-east-1.rds.amazonaws.com:5432/database-2"
    
    return create_engine(conn_str, echo=False, pool_size=10, max_overflow=20)

def get_session():
    engine = get_engine()

    # Cria uma fábrica de sessão vinculada a esta conexão do banco de dados.
    # sessionmaker é uma função/fábrica que produz novas sessões de banco de dados.
    # O parâmetro 'bind' associa o 'engine' (conexão com o banco de dados) a cada sessão criada.
    Session = sessionmaker(bind=engine)
    #SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session()


    #conn_str = "postgresql://learnlink:senha123@dbgrupo2seduc.czf3otuim7ts.us-east-1.rds.amazonaws.com:5432/learnlinkdb"
    # conn_str = "postgresql://learnlink:senha123@dbgrupo2seduc.czf3otuim7ts.us-east-1.rds.amazonaws.com:5432/learnlinkdb"

    # "postgresql://postgres:postgres123@learnlink-database.cglbxr3wjuwg.us-east-1.rds.amazonaws.com:5432/lumDb?connect_timeout=30&pool_timeout=30&socket_timeout=30"
   