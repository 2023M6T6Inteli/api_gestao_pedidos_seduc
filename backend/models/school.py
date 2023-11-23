import json

from .factories import *
from .dao import BaseDAO
from models.entities import *

""" DAO
================================================================================
"""



class SchoolDAO(BaseDAO):

    def create_school(self, map_):
        """
        Add a school to the Database
        """
        entity = SchoolEntity(
            name = map_['name'],
            address = map_['address'],
            cep = map_['cep'],
            cnpj = map_['cnpj']
        )
        return self._session.add(entity)
    
    def update_school(self, id, map_):
        """
        Update a school in the Database
        """
        entity = self._find_entity_by_id(id)
        if entity:
            for key, value in map_.items():
                setattr(entity, key, value)
            self._session.commit()
            return self._build_model_from_entity(entity)
        else:
            return None
        
    def delete_school(self, id):
        """
        Delete a school in the Database
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

    def find_by_cnpj(self, cnpj):
        """
        Finds an instance by cnpj
        """
        entity = self._session.query(SchoolEntity).filter(SchoolEntity.cnpj == cnpj).first()
        if (entity):
            return self._build_model_from_entity(entity)

    # Private methods
    # -------------------------------------------------------------------------

    def _find_entity_by_id(self, id):
        return self._session.query(SchoolEntity).filter(SchoolEntity.id == id).first()

    def _build_model_from_entity(self, entity):
        """
        Build a Student model out of an entity
        """
        school = School(
            id = entity.id,
            name = entity.name,
            address = entity.address,
            cep = entity.cep,
            cnpj = entity.cnpj
        )
        return school

""" Model
================================================================================
"""

class School:

    def __init__(self, id, name, address, cep, cnpj):
        self._id = id
        self._name = name
        self._address = address
        self._cep = cep
        self._cnpj = cnpj

    def id(self):
        return self._id

    def add_id(self):
        self._id = id

    def name(self):
        return self._name

    def add_name(self, name):
        self._name = name

    def cnpj(self):
        return self._cnpj

    def add_cnpj(self, cnpj):
        self._cnpj = cnpj

    def address(self):
        return self._address
    
    def add_address(self, address):
        self._address = address
    
    def cep(self):
        return self._cep
    
    def add_cep(self, cep):
        self._cep = cep

    def jsonify(self, indent=2):
        map_ = self.to_map()
        return json.dumps(map_, indent=indent)

    def to_map(self):
        return {
            "id": self.id(),
            "name": self.name(),
            "adress": self.address(),
            "cep": self.cep(),
            "cnpj": self.cnpj()
        }
    
    def employes(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Finds the associated employes in the database
        """
        if hasattr(self, '_employes'):
            return self._employes

        if not self.id():
            raise Exception("You need an id to get dependencies")

        with SchoolDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.employes

            # Use the factory to get a manager of the associated entities
            employe_dao = EmployeSchoolDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            self._employes = [employe_dao._build_model_from_entity(e) for e in associated_entities]
        return self._employes

    def orders(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Finds the associated orders in the database
        """
        if hasattr(self, '_orders'):
            return self._orders

        if not self.id():
            raise Exception("You need an id to get dependencies")

        with SchoolDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.orders

            # Use the factory to get a manager of the associated entities
            order_dao = OrderDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            self._orders = [order_dao._build_model_from_entity(e) for e in associated_entities]
        return self._orders