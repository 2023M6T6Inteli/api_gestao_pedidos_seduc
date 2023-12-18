import logging
from models import user


class LoginServices:
    
        def login(login_map):
            try:
                with user.UserDAO() as dao:
                    dao.login(login_map)
                return True
            except Exception as e:
                logging.error(f"Erro inesperado ao fazer login: {e}")
                return False