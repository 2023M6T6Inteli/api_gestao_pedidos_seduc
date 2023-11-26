import json

from .factories import *
from .dao import BaseDAO
from models.entities import *

""" DAO
================================================================================
"""

class OrderDAO(BaseDAO):

    def create_order(self, map_):
        """
        Add a order to the Database
        """
        entity = OrderEntity(
            nf = map_['nf'],
            nr =map_['nr'],
            shipment_date = map_['shipment_date'],
            status = map_[Enum(OrderStatus)],
            amount = map_['amount'],
            school_id = map_['school_id'],
            supplier_id = map_['supplier_id'],
            employe_seduc_id = map_['employe_seduc_id'],
        )
        return self._session.add(entity)

    ## FAZER ATUALIZAR PEDIDOS DIFERENTES, NOVOS MAPAS?

    def update_order(self, id, map_):
        """
        Update a order in the Database
        """
        entity = self._find_entity_by_id(id)
        if entity:
            for key, value in map_.items():
                setattr(entity, key, value)
            return self._build_model_from_entity(entity)
        else:
            return None
        
    def delete_order(self, id):
        """
        Delete a order in the Database
        """
        entity = self._find_entity_by_id(id)
        if entity:
            self._session.delete(entity)
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

    def find_by_nr(self, nr):
        """
        Finds an instance by cnr
        """
        entity = self._session.query(OrderEntity).filter(OrderEntity.nr == nr).first()
        if (entity):
            return self._build_model_from_entity(entity)

    # Private methods
    # -------------------------------------------------------------------------

    def _find_entity_by_id(self, id):
        return self._session.query(OrderEntity).filter(OrderEntity.id == id).first()
    
    def _find_entity_by_nr(self, nr):
        return self._session.query(OrderEntity).filter(OrderEntity.nr == nr).first()
    
    def _find_entity_by_supplier_id(self, supplier_id):
        return self._session.query(OrderEntity).filter(OrderEntity.supplier_id == supplier_id).first()
    
    def _find_entity_by_school_id(self, school_id):
        return self._session.query(OrderEntity).filter(OrderEntity.school_id == school_id).first()
    
    def _find_entity_by_transporter_id(self, transporter_id):
        return self._session.query(OrderEntity).filter(OrderEntity.transporter_id == transporter_id).first()
    
    def _find_entity_by_employe_seduc_id(self, employe_seduc_id):
        return self._session.query(OrderEntity).filter(OrderEntity.employe_seduc_id == employe_seduc_id).first()


    # se receber campos vazios e tiver o campo na entidade o que rola
    def _build_model_from_entity(self, entity):
        """
        Build a Student model out of an entity
        """
        order = Order(
            id = entity.id,
            nf = entity.nf,
            nr = entity.nr,
            shipment_date = entity.shipment_date,
            status = entity.Enum(OrderStatus),
            amount = entity.amount,
            supplier_id = entity.supplier_id,
            school_id = entity.school_id,
            transporter_id = entity.transporter_id,
            employe_seduc_id = entity.employe_seduc_id
        )
        return order

""" Model
================================================================================
"""

class Order:

    def __init__(self, id, nf, nr, shipment_date, status, amount, supplier_id, school_id, transporter_id, employe_seduc_id):
        self._id = id
        self._nf = nf
        self._nr = nr
        self._shipment_date = shipment_date
        self._status = status
        self._amount = amount
        self._supplier_id = supplier_id
        self._school_id = school_id
        self._transporter_id = transporter_id
        self._employe_seduc_id = employe_seduc_id


    def id(self):
        return self._id

    def add_id(self, id):
        self._id = id

    def nf(self):
        return self._nf
    
    def add_nf(self, nf):
        self._nf = nf
    
    def nr(self):
        return self._nr
    
    def add_nr(self, nr):
        self._nr = nr
    
    def shipment_date(self):
        return self._shipment_date
    
    def add_shipment_date(self, shipment_date):
        self._shipment_date = shipment_date
    
    def status(self):
        return self._status
    
    def add_status(self, status):
        self._status = status

    def amount(self):
        return self._amount
    
    def add_amount(self, amount):
        self._amount = amount

    def supplier_id(self):
        return self._supplier_id
    
    def add_supplier_id(self, supplier_id):
        self._supplier_id = supplier_id

    def school_id(self):
        return self._school_id
    
    def add_school_id(self, school_id):
        self._school_id = school_id

    def transporter_id(self):
        return self._transporter_id
    
    def add_transporter_id(self, transporter_id):
        self._transporter_id = transporter_id

    def jsonify(self, indent=2):
        map_ = self.to_map()
        return json.dumps(map_, indent=indent)

    def to_map(self):
        return {
            "id": self.id(),
            "nf": self.nf(),
            "nr": self.nr(),
            "shipment_date": self.shipment_date(),
            "status": self.status(),
            "amount": self.amount()
            # "supplier_id": self.supplier_id(),
            # "school_id": self.school_id(),
            # "transporter_id": self.transporter_id(),
            # "employe_seduc_id": self.employe_seduc_id()
        }
    
    def employe_seduc(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Finds the associated employes in the database
        """
        if hasattr(self, '_employes'):
            return self._employes

        if not self.id():
            raise Exception("You need an id to get dependencies")

        with OrderDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.employe_seduc_id

            # Use the factory to get a manager of the associated entities
            employe_seduc_dao = EmployeSeducDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            # # Esse método transforma uma Entity em um Model. Isso é importante porque não podemos deixar um Entity ir pra camada de Negócios
            self._employes = [employe_seduc_dao._build_model_from_entity(e) for e in associated_entities]
        return self._employe_seduc_id

    def transporter(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Finds the associated transporters in the database
        """
        if hasattr(self, '_transporters'):
            return self._transporter_id

        if not self.id():
            raise Exception("You need an id to get dependencies")

        with OrderDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.transporter_id

            # Use the factory to get a manager of the associated entities
            transporter_id_dao = TransporterDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            self._transporters = [transporter_id_dao._build_model_from_entity(e) for e in associated_entities]
        return self._transporter_id
    
    def school(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Finds the associated school in the database
        """
        if hasattr(self, '_school'):
            return self._school_id

        if not self.id():
            raise Exception("You need an id to get dependencies")

        with OrderDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.school_id

            # Use the factory to get a manager of the associated entities
            school_id_dao = SchoolDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            self._school = [school_id_dao._build_model_from_entity(e) for e in associated_entities]
        return self._school
    
    def supplier(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Finds the associated supplier in the database
        """
        if hasattr(self, '_supplier'):
            return self._supplier_id

        if not self.id():
            raise Exception("You need an id to get dependencies")

        with OrderDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.supplier_id

            # Use the factory to get a manager of the associated entities
            supplier_id_dao = SupplierDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            self._supplier = [supplier_id_dao._build_model_from_entity(e) for e in associated_entities]
        return self._supplier