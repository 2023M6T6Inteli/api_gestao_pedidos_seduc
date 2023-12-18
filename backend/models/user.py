import json
import logging

from .factories import *
from .dao import BaseDAO
from models.entities import *


class UserDAO(BaseDAO):

    def login(self, login_map):
        email = login_map["email"]
        password = login_map["password"]
        try:
            sucess = self._session.query(UserEntity).filter_by(UserEntity.email == email & UserEntity.password == password).first()
    
            if sucess:
                return True
        except Exception as e:
            logging.error(f"Erro inesperado ao fazer login: {e}")
            return False
    
