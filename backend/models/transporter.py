import json
import logging

from models.supplier import SupplierDAO

from .factories import *
from .dao import BaseDAO
from models.entities import *

""" DAO
================================================================================
"""


class TransporterDAO(BaseDAO):

    def create_transporter(self, map_):
        """
        Add a transporter to the Database
        """
        entity = TransporterEntity(
            name = map_['name'],
            address = map_['address'],
            cep = map_['cep'],
            cnpj = map_['cnpj'],
            supplier_id=map_.get('supplier_id')
        )
        return self._session.add(entity)
    
    def create_transporters(self, transporters_data):
        transporters_entities = []
        for map_ in transporters_data:
            entity = TransporterEntity(
                name=map_['name'],
                address=map_['address'],
                cep=map_['cep'],
                cnpj=map_['cnpj'],
                supplier_id=map_.get('supplier_id')
            )
            transporters_entities.append(entity)

        self._session.add_all(transporters_entities)
    
    # Entender como passo o supplier para ele??

    def update_transporter(self, id, map_):
        """
        Update a transporter in the Database
        """
        entity = self._find_entity_by_id(id)
        if entity:
            for key, value in map_.items():
                setattr(entity, key, value)
            return self._build_model_from_entity(entity)
        else:
            return None
        
    def delete_transporter(self, id):
        """
        Delete a transporter in the Database
        """
        entity = self._find_entity_by_id(id)
        if entity:
            self._session.delete(entity)
            return True
        else:
            return False
        
    def delete_all_transporters(self):
        entities = self.find_all_entity()
        for entity in entities:
            self._session.delete(entity)
        return True
    
    def find_all(self):
        logging.error(f"entrou find_all dao")
        entities = self.find_all_entity()
        logging.error(f"passou find_all dao")
        return self._build_models_from_entities(entities)

    def find_by_id(self, id):
        """
        Finds an instance by id
        """
        logging.error(f"entrou find_by_id dao")
        entity = self._find_entity_by_id(id)
        logging.error(f"passou find_by_id dao", entity)
        if (entity):
            return self._build_model_from_entity(entity)

    def find_by_cnpj(self, cnpj):
        """
        Finds an instance by cnpj
        """
        entity = self._session.query(TransporterEntity).filter(TransporterEntity.cnpj == cnpj).first()
        if (entity):
            return self._build_model_from_entity(entity)
        
    def get_supplier(self, supplier_id):
        supplier_dao = SupplierDAO()
        if not supplier_id:
            return None
        with SupplierDAO() as supplier_dao:  # Inicializa o SupplierDAO aqui
            supplier_entity = supplier_dao.find_by_id(supplier_id)
            return supplier_entity

    # Private methods
    # -------------------------------------------------------------------------

    def find_all_entity(self):
        return self._session.query(TransporterEntity).all()

    def _find_entity_by_id(self, id):
        return self._session.query(TransporterEntity).filter(TransporterEntity.id == id).first()

    def _build_model_from_entity(self, entity):
        """
        Build a Student model out of an entity
        """
        supplier = self.get_supplier(entity.supplier_id)
        transporter = Transporter(
            id = entity.id,
            name = entity.name,
            address = entity.address,
            cep = entity.cep,
            cnpj = entity.cnpj,
            supplier = supplier
            # supplier_id = entity.supplier_id   
            # Crio outra _build_ que contenha os relacionamentos?
            # employes = entity.employes,
            # orders = entity.orders
        )
        return transporter
    
    def _build_models_from_entities(self, entities):
        transporters = []
        for entity in entities:
            transporters.append(self._build_model_from_entity(entity))
        return transporters

""" Model
================================================================================
"""

class Transporter:

    def __init__(self, id, name, address, cep, cnpj, supplier):
        self._id = id
        self._name = name
        self._address = address
        self._cep = cep
        self._cnpj = cnpj
        self._supplier = supplier
        # self._supplier_id = supplier_id

    def id(self):
        return self._id

    def add_id(self, id):
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

    def supplier_id(self):
        return self._supplier_id
    
    def add_supplier_id(self, supplier_id):
        self._supplier_id = supplier_id

    def supplier(self):
        return self._supplier

    def jsonify(self, indent=2):
        map_ = self.to_map()
        return json.dumps(map_, indent=indent)

    def to_map(self):
        supplier_map = self._supplier.to_map() if self._supplier else None
        return {
            "id": self.id(),
            "name": self.name(),
            "address": self.address(),
            "cep": self.cep(),
            "cnpj": self.cnpj(),
            "supplier": supplier_map
            # "supplier_id": self.supplier_id()
        }
    
    def employes(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Finds the associated employes in the database
        """
        if hasattr(self, '_employes'):
            return self._employes

        if not self.id():
            raise Exception("You need an id to get dependencies")

        with TransporterDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.employes

            # Use the factory to get a manager of the associated entities
            employe_dao = EmployeTransporterDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            # Esse método transforma uma Entity em um Model. Isso é importante porque não podemos deixar um Entity ir pra camada de Negócios
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

        with TransporterDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.orders

            # Use the factory to get a manager of the associated entities
            order_dao = OrderDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            self._orders = [order_dao._build_model_from_entity(e) for e in associated_entities]
        return self._orders