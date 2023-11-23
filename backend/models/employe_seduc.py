import json

from .factories import *
from .dao import BaseDAO
from models.entities import *

""" DAO
================================================================================
"""
# EmployeSeducDAO terá todas as funcionalidades de BaseDAO, como gerenciamento de sessões de banco de dados.
class EmployeSeducDAO(BaseDAO):

    def create_employe_seduc(self, map_):
        """
        Add a employe_seduc to the Database
        """
        # Cria uma entidade estudante
        employe_seduc_entity = EmployeSeducEntity(
            id = map_['id'],
            name = map_['name'],
            cpf = map_['cpf'],
            email = map_['email'],
            password = map_['password'],
            role = map_['role'],
            celular = map_['celular'],
        )

        return self._session.add(employe_seduc_entity)
    
    def update_employe_seduc(self, map_):
        """
        Update a employe_seduc to the Database
        """
        entity = self._find_entity_by_id(id)
        if entity:
            for key, value in map_.items():
                setattr(entity, key, value)
                self._session.commit()
            return self._build_model_from_entity(entity)
        else:
            return None
        
    def delete_employe_seduc(self, id):
        """
        Delete a employe_seduc to the Database
        """
        entity = self._find_entity_by_id(id)
        if entity:
            self._session.delete(entity)
            self._session.commit()
            return True
        else:
            return False

    def find_by_id(self, id):
        """
        Finds an instance by id
        """
        entity = self._find_entity_by_id(id)
        if (entity):
            return self._build_model_from_entity(entity)

    def find_by_cpf(self, cpf):
        """
        Finds an instance by cpf
        """
        entity = self._find_entity_by_cpf(cpf)
        if (entity):
            return self._build_model_from_entity(entity)

    # Private methods
    # -------------------------------------------------------------------------

    def _find_entity_by_id(self, id):
        return self._session.query(EmployeSeducEntity).filter(EmployeSeducEntity.id == id).first()

    def _find_entity_by_cpf(self, cpf):
        return self._session.query(EmployeSeducEntity).filter(EmployeSeducEntity.cpf == cpf).first()

    def _build_model_from_entity(self, entity):
        """
        Build a EmployeSeduc model out of an entity
        """
        employe_seduc = EmployeSeduc(
            id = entity.id,
            name = entity.name,
            cpf = entity.cpf,
            email = entity.email,
            password = entity.password,
            role = entity.role,
            celular = entity.celular,
        )
        return employe_seduc




""" Model
================================================================================
"""
# Esta classe representa o modelo de um estudante em seu sistema. Ela possui atributos como id, ra, name e courses, além de métodos para 
# manipular esses atributos e para converter os dados do estudante em diferentes formatos, como um dicionário ou JSON.

# O modelo EmployeSeduc é uma representação mais amigável e prática dos dados de um estudante, que pode ser usada em outras partes do seu 
# aplicativo, como interfaces de usuário, lógica de negócios ou comunicação entre diferentes componentes do sistema.
class EmployeSeduc:

    def __init__(self, id, name, cpf, email, password, role, celular):
            self._id = id
            self.name = name
            self.cpf = cpf
            self.email = email
            self.password = password
            self.role = role
            self.celular = celular


    def id(self):
        return self._id

    def add_id(self):
        self._id = id

    def name(self):
        return self._name

    def add_name(self, name):
        self._name = name

    def cpf(self):
        return self._cpf

    def add_cpf(self, cpf):
        self._cpf = cpf

    def email(self):
        return self._email
    
    def add_email(self, email):
        self._email = email
    
    def password(self):
        return self._password
    
    def add_password(self, password):
        self._password = password
    
    def role(self):
        return self._role
    
    def add_role(self, role):
        self._role = role
    
    def celular(self):
        return self._celular

    def jsonify(self, indent=2):
        map_ = self.to_map()
        return json.dumps(map_, indent=indent)

    def to_map(self):
        return {
            "id": self.id(),
            "name": self.name(),
            "cpf": self.cpf(),
            "email": self.email(),
            "password": self.password(),
            "role": self.role(),
            "celular": self.celular(),
        }
    
