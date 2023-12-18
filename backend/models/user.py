import json
import logging

from .factories import *
from .dao import BaseDAO
from models.entities import *
from models.employe_school import EmployeSchoolDAO
from models.employe_transporter import EmployeTransporterDAO
from models.employe_supplier import EmployeSupplierDAO


class UserDAO(BaseDAO):

    def login(self, login_map):
        email = login_map["email"]
        password = login_map["password"]
        try:
            logging.error(f"entrou login dao")
            sucess = self._session.query(UserEntity).filter(UserEntity.email == email, UserEntity.password == password).first()

    
            if sucess:
                try:
                    if "school" in email:
                        with EmployeSchoolDAO() as dao:
                            return dao.find_school_id(email)
                    elif "transporter" in email:
                        with EmployeTransporterDAO() as dao:
                            return dao.find_transporter_id(email)
                    elif "supplier" in email:
                        with EmployeSupplierDAO() as dao:
                            return dao.find_supplier_id(email)
                    elif "seduc" in email:
                        return "seduc"
                except Exception as e:
                    logging.error(f"Usuário com email fora do padrão: {e}")
                    return False

                
        except Exception as e:
            logging.error(f"Erro inesperado ao fazer login: {e}")
            return False
    
