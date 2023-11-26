from models.db_credentials import get_session, get_engine
from db_resetter import drop_n_create_db

#e = get_session()
#print(e)

drop_n_create_db()