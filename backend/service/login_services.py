import logging
from models import user


class LoginServices:
    
        def login(self, login_map):
            logging.error(f"entrou login services")
            try:
                logging.debug("LoginServices.login")
                with user.UserDAO() as dao:
                    return dao.login(login_map)
                
            except Exception as e:
                logging.error(f"Erro inesperado ao fazer login: {e}")
                return False