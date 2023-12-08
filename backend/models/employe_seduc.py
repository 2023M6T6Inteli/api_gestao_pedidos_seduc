import json
import logging

from .factories import *
from .dao import BaseDAO
from models.entities import *

""" DAO
================================================================================
"""
# EmployeSeducDAO terá todas as funcionalidades de BaseDAO, como gerenciamento de sessões de banco de dados.
class EmployeSeducDAO(BaseDAO):

    def create_employe_seduc(self, map_):
        # Cria uma entidade estudante
        employe_seduc_entity = EmployeSeducEntity(

            name = map_['name'],
            cpf = map_['cpf'],
            email = map_['email'],
            password = map_['password'],
            role = map_['role'],
            celular = map_['celular'],
        )
        logging.error(f"entrou create_employe_seduc dao")
        return self._session.add(employe_seduc_entity)
    
    def update_employe_seduc(self, id, map_):
        logging.error(f"entrou update_employe_seduc dao")
        entity = self._find_entity_by_id(id)
        if entity:
            for key, value in map_.items():
                setattr(entity, key, value)
            return self._build_model_from_entity(entity)
        else:
            return None
        
    def delete_employe_seduc(self, id):
        entity = self._find_entity_by_id(id)
        if entity:
            self._session.delete(entity)
            return True
        else:
            return False

    def find_all(self):
        entities = self.find_all_entity()
        return self._build_models_from_entities(entities)

    def find_by_id(self, id):
        logging.error(f"entrou find_by_id dao")
        entity = self._find_entity_by_id(id)
        logging.error(f"passou find_by_id dao")
        if (entity):
            return self._build_model_from_entity(entity)

    def find_by_cpf(self, cpf):
        entity = self._find_entity_by_cpf(cpf)
        if (entity):
            return self._build_model_from_entity(entity)

    # Private methods
    # -------------------------------------------------------------------------

    def find_all_entity(self):
        return self._session.query(EmployeSeducEntity).all()

    def _find_entity_by_id(self, id):
        logging.error(f"entrou _find_entity_by_id dao")
        return self._session.query(EmployeSeducEntity).get(id)

    def _find_entity_by_cpf(self, cpf):
        result = self._session.query(EmployeSeducEntity).filter(EmployeSeducEntity.cpf == cpf).first()
        return result

    def _build_model_from_entity(self, entity):
        logging.error(f"entrou _build_model_from_entity dao")
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
    
    def _build_models_from_entities(self, entities):
        """
        Build a list of EmployeSeduc models out of a list of entities
        """
        employe_seducs = []
        for entity in entities:
            employe_seducs.append(self._build_model_from_entity(entity))
        return employe_seducs

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
            self._name = name
            self._cpf = cpf
            self._email = email
            self._password = password
            self._role = role
            self._celular = celular

    @property
    def id(self):
        return self._id

    def add_id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    def add_name(self, name):
        self._name = name

    @property
    def cpf(self):
        return self._cpf

    def add_cpf(self, cpf):
        self._cpf = cpf

    @property
    def email(self):
        return self._email
    
    def add_email(self, email):
        self._email = email

    @property
    def password(self):
        return self._password
    
    def add_password(self, password):
        self._password = password
    
    @property
    def role(self):
        return self._role
    
    def add_role(self, role):
        self._role = role
    
    @property
    def celular(self):
        return self._celular
    
    def add_celular(self, celular):
        self._celular = celular

    def jsonify(self, indent=2):
        map_ = self.to_map()
        for key, value in map_.items():
            if isinstance(value, datetime):
                map_[key] = value.isoformat()
            elif isinstance(value, str):
                map_[key] = value.encode('utf-8').decode('utf-8')
        return json.dumps(map_, indent=indent, ensure_ascii=False)

    def to_map(self):
        return {
            "id": self._id,
            "name": self._name,
            "cpf": self._cpf,
            "email": self._email,
            "password": self._password,
            "role": self._role,
            "celular": self._celular,
        }
    
