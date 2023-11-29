import json

from .factories import *
from .dao import BaseDAO
from models.entities import *


""" DAO
================================================================================
"""

class SupplierDAO(BaseDAO):

    def create_supplier(self, map_):
        """
        Add a supplier to the Database
        """
        entity = SupplierEntity(
            name = map_['name'],
            address = map_['address'],
            cep = map_['cep'],
            cnpj = map_['cnpj']
        )
        return self._session.add(entity)
    
    def create_suppliers(self, suppliers_data):
        suppliers_entities = []
        for map_ in suppliers_data:
            entity = SupplierEntity(
                name=map_['name'],
                address=map_['address'],
                cep=map_['cep'],
                cnpj=map_['cnpj']
            )
            suppliers_entities.append(entity)

        self._session.add_all(suppliers_entities)

    def update_supplier(self, id, map_):
        """
        Update a supplier in the Database
        """
        entity = self._find_entity_by_id(id)
        if entity:
            for key, value in map_.items():
                setattr(entity, key, value)
            return self._build_model_from_entity(entity)
        else:
            return None
        
    def delete_supplier(self, id):
        """
        Delete a supplier in the Database
        """
        entity = self._find_entity_by_id(id)
        if entity:
            self._session.delete(entity)
            return True
        else:
            return False
        
    def delete_all_suppliers(self):
        entities = self.find_all_entity()
        for entity in entities:
            self._session.delete(entity)
        return True
    
    def find_all(self):
        entities = self.find_all_entity()
        return self._build_models_from_entities(entities)

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
        entity = self._session.query(SupplierEntity).filter(SupplierEntity.cnpj == cnpj).first()
        if (entity):
            return self._build_model_from_entity(entity)
        
    def find_transporter_by_supplier_id(self, supplier_id):
        transporters = self._session.query(TransporterEntity).filter(TransporterEntity.supplier_id == supplier_id).all()
        return [self._build_model_from_entity(transporter) for transporter in transporters]
        

    # Private methods
    # -------------------------------------------------------------------------

    def find_all_entity(self):
        return self._session.query(SupplierEntity).all()

    def _find_entity_by_id(self, id):
        return self._session.query(SupplierEntity).filter(SupplierEntity.id == id).first()
    
    def find_entity_transporter_by_supplier_id(self, supplier_id):
        transporters = self._session.query(TransporterEntity).filter(TransporterEntity.supplier_id == supplier_id).all()
        if (transporters):
            return transporters
        return []

    def _build_model_from_entity(self, entity):
        """
        Build a Student model out of an entity
        """
        supplier = Supplier(
            id = entity.id,
            name = entity.name,
            address = entity.address,
            cep = entity.cep,
            cnpj = entity.cnpj
            # Crio outra _build_ que contenha os relacionamentos? Ou isso fica pro serviço?
            # employes = entity.employes,
            # orders = entity.orders
        )
        return supplier
    
    def _build_models_from_entities(self, entities):
        suppliers = []
        for entity in entities:
            suppliers.append(self._build_model_from_entity(entity))
        return suppliers

""" Model
================================================================================
"""

class Supplier:

    def __init__(self, id, name, address, cep, cnpj):
        self._id = id
        self._name = name
        self._address = address
        self._cep = cep
        self._cnpj = cnpj

    def id(self):
        return self._id

    def add_id(self, id):
        self._id = id

    def name(self):
        return self._name

    def add_name(self, name):
        self._name = name

    def address(self):
        return self._address

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

    def get_transporters(self):
        with SupplierDAO() as dao:
            transporters = dao.find_transporter_by_supplier_id(self.id())
            return [t.to_map() for t in transporters] 

    def jsonify(self, indent=2):
        map_ = self.to_map()
        map_["status"] = self.status().to_dict()
        for key, value in map_.items():
            if isinstance(value, datetime):
                map_[key] = value.isoformat()
            elif isinstance(value, str):
                map_[key] = value.encode('utf-8').decode('utf-8')
        return json.dumps(map_, indent=indent, ensure_ascii=False)

    # Função para serializar o estado do objeto para formatos que podem ser facilmente transmitidos ou armazenados, como JSON,
    def to_map(self):
        return {
            "id": self.id(),
            "name": self.name(),
            "address": self.address(),
            "cep": self.cep(),
            "cnpj": self.cnpj(),
            "transporters": self.get_transporters()
        }
    
    def employes(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Finds the associated employes in the database
        """
        if hasattr(self, '_employes'):
            return self._employes

        if not self.id():
            raise Exception("You need an id to get dependencies")

        with SupplierDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.employes

            # Use the factory to get a manager of the associated entities
            employe_dao = EmployeSupplierDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            # Esse método transforma uma Entity em um Model. Isso é importante porque não podemos deixar um Entity ir pra camada de Negócios
            self._employes = [employe_dao._build_model_from_entity(e) for e in associated_entities]
        return self._employes

    def transporters(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Finds the associated transporters in the database
        """
        if hasattr(self, '_transporters'):
            return self._transporters

        if not self.id():
            raise Exception("You need an id to get dependencies")

        with SupplierDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.transporters

            # Use the factory to get a manager of the associated entities
            transporter_dao = TransporterDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            self._transporters = [transporter_dao._build_model_from_entity(e) for e in associated_entities]
        return self._transporters

    def orders(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Finds the associated orders in the database
        """
        if hasattr(self, '_orders'):
            return self._orders

        if not self.id():
            raise Exception("You need an id to get dependencies")

        with SupplierDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.orders

            # Use the factory to get a manager of the associated entities
            order_dao = OrderDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            self._orders = [order_dao._build_model_from_entity(e) for e in associated_entities]
        return self._orders