import json
import logging

from .factories import *
from .dao import BaseDAO
from models.entities import *

""" DAO
================================================================================
"""
# EmployeTransporterDAO terá todas as funcionalidades de BaseDAO, como gerenciamento de sessões de banco de dados.
class EmployeTransporterDAO(BaseDAO):

    def create_employe_transporter(self, map_):
        """
        Add a employe_transporter to the Database
        """
        # Cria uma entidade estudante
        employe_transporter_entity = EmployeTransporterEntity(

            name = map_['name'],
            cpf = map_['cpf'],
            email = map_['email'],
            password = map_['password'],
            transporter_id = map_['transporter_id'],
            celular = map_['celular'],
        )

        # Adiciona a sessão para que seja inserido ao banco de daos
        return self._session.add(employe_transporter_entity)
    
    def update_employe_transporter(self, id, map_):
        """
        Update a employe_transporter to the Database
        """
        entity = self._find_entity_by_id(id)
        if entity:
            for key, value in map_.items():
                setattr(entity, key, value)
            return self._build_model_from_entity(entity)
        else:
            return None
        
    def delete_employe_transporter(self, id):  
        """
        Delete a employe_transporter to the Database
        """
        entity = self._find_entity_by_id(id)
        if entity:
            self._session.delete(entity)
            return True
        else:
            return False

    def find_all(self):
        #logging.error(f"entrou find_all dao")
        entities = self.find_all_entity()
        #logging.error(f"passou find_all dao")
        return self._build_models_from_entities(entities)

    def find_by_id(self, id):
        """
        Finds an instance by id
        """
        #logging.error(f"entrou find_by_id dao")
        entity = self._find_entity_by_id(id)
        #logging.error(f"passou find_by_id dao", entity)
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

    def find_all_entity(self):
        #logging.error(f"entrou find_all_entyty")
        return self._session.query(EmployeTransporterEntity).all()

    def _find_entity_by_id(self, id):
        #logging.error(f"entrou find_entity_by_id")
        return self._session.query(EmployeTransporterEntity).filter(EmployeTransporterEntity.id == id).first()

    def _find_entity_by_cpf(self, cpf):
        return self._session.query(EmployeTransporterEntity).filter(EmployeTransporterEntity.cpf == cpf).first()

    def _build_model_from_entity(self, entity):
        """
        Build a EmployeTransporter model out of an entity
        """
        employe_transporter = EmployeTransporter(
            id = entity.id,
            name = entity.name,
            cpf = entity.cpf,
            email = entity.email,
            password = entity.password,
            celular = entity.celular,
            transporter_id = entity.transporter_id,
        )
        #logging.error(f"passou build_model_from_entity,  employe_transporter: {employe_transporter}")
        return employe_transporter
    
    def _build_models_from_entities(self, entities):
        employe_transporters = []
        for entity in entities:
            employe_transporter = self._build_model_from_entity(entity)
            employe_transporters.append(employe_transporter)
        #logging.error(f"passou build_models_from_entities,  employe_transporters: {employe_transporters}")
        return employe_transporters

    def _map_to_transporter_entities(self, transporter_ids):
        """
        Converts the courses ids in the map to their entities
        """
        mng = TransporterDAOFactory.create(self.session())
        entities = []
        for id in transporter_ids:
            entity = mng._find_entity_by_id(id)
            entities.append(entity)
        return entities
    
    def _find_transporter_entity_by_id(self, id):
        transporter_dao = TransporterDAOFactory.create(self.session())
        return transporter_dao._find_entity_by_id(id)


""" Model
================================================================================
"""
# Esta classe representa o modelo de um estudante em seu sistema. Ela possui atributos como id, ra, name e courses, além de métodos para 
# manipular esses atributos e para converter os dados do estudante em diferentes formatos, como um dicionário ou JSON.

# O modelo EmployeTransporter é uma representação mais amigável e prática dos dados de um estudante, que pode ser usada em outras partes do seu 
# aplicativo, como interfaces de usuário, lógica de negócios ou comunicação entre diferentes componentes do sistema.
class EmployeTransporter:

    def __init__(self, id, name, cpf, email, password, celular, transporter_id):
            self._id = id
            self._name = name
            self._cpf = cpf
            self._email = email
            self._password = password
            self._celular = celular
            self._transporter_id = transporter_id

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
    def celular(self):
        return self._celular
    
    def add_celular(self, celular):
        self._celular = celular

    @property
    def transporter_id(self):
        return self._transporter_id
    
    def add_transporter_id(self, transporter_id):    
        self._transporter_id = transporter_id

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
            "celular": self._celular,
            "transporter_id": self._transporter_id,
        }
    


    
    # def transporters(self, session=None, commit_on_exit=True, close_on_exit=True):
    #     """
    #     Finds the associated models in the database
    #     """
    #     if (self._transporters):
    #         return self._transporters

    #     if (not self.id()):
    #         raise Exception("You need an id to get dependencies")

    #     with EmployeTransporterDAO(session, commit_on_exit, close_on_exit) as dao:
    #         # Obtain the entity of this model
    #         entity = dao._find_entity_by_id(self.id())

    #         # Finds the associated entities
    #         associated_entities = entity.transporters

    #         # Use the factory to get a manager of the associated entities
    #         transporter_dao = TransporterDAOFactory.create(dao.session())

    #         # A list of the models of the associated entities
    #         self._transporters = [transporter_dao._build_model_from_entity(e) for e in associated_entities]
    #     return self._transporters