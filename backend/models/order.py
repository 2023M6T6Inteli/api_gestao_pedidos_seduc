import json
import logging
from models.employe_seduc import EmployeSeducDAO
from models.school import SchoolDAO
from models.transporter import TransporterDAO

from models.supplier import SupplierDAO

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
            status = OrderStatus(map_['status']),
            amount = map_['amount'],
            school_id = map_['school_id'],
            supplier_id = map_['supplier_id'],
            employe_seduc_id = map_['employe_seduc_id'],
            transporter_id = map_.get('transporter_id')
        )
        return self._session.add(entity)
    
    def create_orders(self, orders_data):
        orders_entities = []
        for map_ in orders_data:
            entity = OrderEntity(
                nf = map_['nf'],
                nr =map_['nr'],
                shipment_date = map_['shipment_date'],
                status = OrderStatus(map_['status']),
                amount = map_['amount'],
                school_id = map_['school_id'],
                supplier_id = map_['supplier_id'],
                employe_seduc_id = map_['employe_seduc_id'],
                transporter_id = map_.get('transporter_id')
            )
            orders_entities.append(entity)

        self._session.add_all(orders_entities)

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
        
    def find_by_id_with_dependencies(self, id):
        """
        Finds an instance by id with all dependencies loaded
        """
        entity = self._find_entity_by_id(id)
        if (entity):
            return self._build_model_from_entity_with_dependencies(entity)

    def find_by_nr(self, nr):
        """
        Finds an instance by nr
        """
        entity = self._session.query(OrderEntity).filter(OrderEntity.nr == nr).first()
        if (entity):
            return self._build_model_from_entity(entity)
    
        
    """
    Query para preenchimentos dos feeds ('pedidos' e 'histórico' do usuário employe_Seduc), algumas querys dos outros users podem ser usado na tela do employe_Seduc como filtro.
    Por exemplo: para filtrar todos pedidos de fornecedor
    """

    def find_all_orders_by_employe_seduc_id(self, employe_seduc_id):
        entities = self.find_all_entities_by_employe_seduc_id(employe_seduc_id)
        if (entities):
            return self._build_models_from_entities(entities)
        
    def find_all_orders_by_multiple_status(self, status):
        logging.debug("entrou find_All_orders_multiple na model order.")
        entities = self.find_all_entities_by_multiple_status(status)
        logging.debug("passou entities na model order.")
        if (entities):
            return self._build_models_from_entities(entities)
        
    def find_all_orders_by_status(self, status):
        entities = self.find_all_entities_by_status(status)
        if (entities):
            return self._build_models_from_entities(entities)
    
    """
    Query para preenchimentos dos feeds dos suppliers
    """

    def find_all_orders_by_multiple_status_and_supplier_id(self, status, supplier_id):
        entities = self.find_all_entities_by_multiple_status_and_supplier_id(status, supplier_id)
        if (entities):
            return self._build_models_from_entities(entities)
        
    def find_all_orders_by_supplier_id(self, supplier_id):
        entities = self.find_all_entities_by_supplier_id(supplier_id)
        if (entities):
            return self._build_models_from_entities(entities)
    
    """
    Query para preenchimentos dos feeds das escolas
    """

    def find_all_orders_by_multiple_status_and_school_id(self, status, school_id):
        entities = self.find_all_entities_by_multiple_status_and_school_id(status, school_id)
        if (entities):
            return self._build_models_from_entities(entities)
        
    def find_all_orders_by_school_id(self, school_id):
        entities = self.find_all_entities_by_school_id(school_id)
        if (entities):
            return self._build_models_from_entities(entities)
        
    """
    Query para preenchimentos dos feeds dos transporters
    """

    def find_all_orders_by_multiple_status_and_transporter_id(self, status, transporter_id):
        entities = self.find_all_entities_by_multiple_status_and_transporter_id(status, transporter_id)
        if (entities):
            return self._build_models_from_entities(entities)
        
    def find_all_orders_by_transporter_id(self, transporter_id):
        entities = self.find_all_entities_by_transporter_id(transporter_id)
        if (entities):
            return self._build_models_from_entities(entities)
        
    

    # Private methods
    # -------------------------------------------------------------------------


    def find_all_entity(self):
        return self._session.query(OrderEntity).all()
        
    def _find_entity_by_id(self, id):
        return self._session.query(OrderEntity).filter(OrderEntity.id == id).first()
    
    def _find_entity_by_nr(self, nr):
        return self._session.query(OrderEntity).filter(OrderEntity.nr == nr).first()
    
    def get_supplier(self, supplier_id):
        supplier_dao = SupplierDAO()
        if not supplier_id:
            return None
        with SupplierDAO() as supplier_dao:
            supplier_entity = supplier_dao.find_by_id(supplier_id)
            return supplier_entity
        
    def get_transporter(self, transporter_id):
        transporter_dao = TransporterDAO()
        if not transporter_id:
            return None
        with TransporterDAO() as transporter_dao:
            transporter_entity = transporter_dao.find_by_id(transporter_id)
            return transporter_entity
        
    def get_school(self, school_id):
        school_dao = SchoolDAO()
        if not school_id:
            return None
        with SchoolDAO() as school_dao:
            school_entity = school_dao.find_by_id(school_id)
            return school_entity
        
    def get_employe_seduc(self, employe_seduc_id):
        employe_seduc_dao = EmployeSeducDAO()
        if not employe_seduc_id:
            return None
        with EmployeSeducDAO() as employe_seduc_dao:
            employe_seduc_entity = employe_seduc_dao.find_by_id(employe_seduc_id)
            return employe_seduc_entity

    """
    Query para preenchimentos dos feeds ('pedidos' e 'histórico' do usuário employe_Seduc), algumas querys dos outros users podem ser usado na tela do employe_Seduc como filtro.
    Por exemplo: para filtrar todos pedidos de fornecedor
    """
    def find_all_entity(self):
        return self._session.query(OrderEntity).all()
    
    def find_all_entities_by_status(self, status):
        return self._session.query(OrderEntity).filter(OrderEntity.status == status).all()
    
    def find_all_entities_by_multiple_status(self, status):
        logging.debug("entrou find_All_entities_multiple na model order.")
        return self._session.query(OrderEntity).filter(OrderEntity.status.in_(status)).all()
    
    def find_all_entities_by_employe_seduc_id(self, employe_seduc_id):
        return self._session.query(OrderEntity).filter(OrderEntity.employe_seduc_id == employe_seduc_id).all()
    
    """
    Query para preenchimentos dos feeds dos suppliers
    """
    def find_all_entities_by_multiple_status_and_supplier_id(self, status, supplier_id):
        return self._session.query(OrderEntity).filter(OrderEntity.status.in_(status), OrderEntity.supplier_id == supplier_id).all()
    
    def find_all_entities_by_supplier_id(self, supplier_id):
        return self._session.query(OrderEntity).filter(OrderEntity.supplier_id == supplier_id).all()
       
    """
    Query para preenchimentos dos feeds das escolas
    """
    
    def find_all_entities_by_school_id(self, school_id):
        return self._session.query(OrderEntity).filter(OrderEntity.school_id == school_id).all()
    
    def find_all_entities_by_multiple_status_and_school_id(self, status, school_id):
        return self._session.query(OrderEntity).filter(OrderEntity.status.in_(status), OrderEntity.school_id == school_id).all()
    
    """
    Query para preenchimentos dos feeds dos transporters
    """
    
    def find_all_entities_by_transporter_id(self, transporter_id):
        return self._session.query(OrderEntity).filter(OrderEntity.transporter_id == transporter_id).all()
    
    def find_all_entities_by_multiple_status_and_transporter_id(self, status, transporter_id):
        return self._session.query(OrderEntity).filter(OrderEntity.status.in_(status), OrderEntity.transporter_id == transporter_id).all()


    # se receber campos vazios e tiver o campo na entidade o que rola
    def _build_model_from_entity(self, entity):
        """
        Build a Orders model out of an entity
        """
        supplier = self.get_supplier(entity.supplier_id)
        school = self.get_school(entity.school_id)
        transporter = self.get_transporter(entity.transporter_id)

        order = Order(
            id = entity.id,
            nf = entity.nf,
            nr = entity.nr,
            shipment_date = entity.shipment_date,
            status = entity.status,
            amount = entity.amount,
            supplier = supplier,
            school = school,
            transporter= transporter,
            employe_seduc_id = entity.employe_seduc_id
            
            # supplier_id = entity.supplier_id,
            # school_id = entity.school_id,
            # transporter_id = entity.transporter_id,
            # employe_seduc_id = entity.employe_seduc_id
        )
        return order
    
    def _build_models_from_entities(self, entities):
        """
        Build a list of Orders models out of a list of entities
        """
        orders = []
        for entity in entities:
            order = self._build_model_from_entity(entity)
            orders.append(order)
        return orders
    
    # def _build_model_from_entity_with_dependencies(self, entity):
    #     """
    #     Build a Orders model out of an entity with all dependencies loaded
    #     """
    #     order = self._build_model_from_entity(entity)
    #     order.employe_seduc = self.find_employe_seduc_by_id(entity.employe_seduc_id)
    #     order.transporter = self.find_transporter_by_id(entity.transporter_id)
    #     order.supplier = self.find_supplier_by_id(entity.supplier_id)
    #     order.school = self.find_school_by_id(entity.school_id)
    #     return order

""" Model
================================================================================
"""

class Order:

    def __init__(self, id, nf, nr, shipment_date, status, amount, supplier, school, transporter, employe_seduc_id):
        self._id = id
        self._nf = nf
        self._nr = nr
        self._shipment_date = shipment_date
        self._status = status
        self._amount = amount
        self._supplier = supplier
        self._school = school
        self._transporter = transporter
        self._employe_seduc_id = employe_seduc_id
        # self._supplier_id = supplier_id
        # self._school_id = school_id
        # self._transporter_id = transporter_id
        # self._employe_seduc_id = employe_seduc_id


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

    def supplier(self):
        return self._supplier

    def school_id(self):
        return self._school_id
    
    def add_school_id(self, school_id):
        self._school_id = school_id

    def school(self):
        return self._school

    def transporter_id(self):
        return self._transporter_id
    
    def add_transporter_id(self, transporter_id):
        self._transporter_id = transporter_id
    
    def transporter(self):
        return self._transporter

    def employe_seduc_id(self):
        return self._employe_seduc_id
    
    def add_employe_seduc_id(self, employe_seduc_id):
        self._employe_seduc_id = employe_seduc_id


    def jsonify(self, indent=2):
        map_ = self.to_map()
        map_["status"] = self.status().to_dict()
        for key, value in map_.items():
            if isinstance(value, datetime):
                map_[key] = value.isoformat()
        return json.dumps(map_, indent=indent)

    def to_map(self):
        supplier_map = self._supplier.to_map() if self._supplier else None
        school_map = self._school.to_map() if self._school else None
        transporter_map = self._transporter.to_map() if self._transporter else None
        return {
            "id": self.id(),
            "nf": self.nf(),
            "nr": self.nr(),
            "shipment_date": self.shipment_date(),
            "status": self.status().to_dict(),
            "amount": self.amount(),
            "supplier": supplier_map,
            "school": school_map,
            "transporter": transporter_map,
            "employe_seduc_id": self.employe_seduc_id()
        }
    


    # def find_school_by_id(self, school_id):
    #     school_dao = SchoolDAO()
    #     if not school_id:
    #         return None
    #     with SchoolDAO() as school_dao:
    #         school_entity = school_dao.find_by_id(school_id)
    #         return school_entity
        
    # def find_transporter_by_id(self, transporter_id):
    #     transporter_dao = TransporterDAO()
    #     if not transporter_id:
    #         return None
    #     with TransporterDAO() as transporter_dao:
    #         transporter_entity = transporter_dao.find_by_id(transporter_id)
    #         return transporter_entity
        
    
    # def find_employe_seduc_by_id(self, employe_seduc_id):
    #     employe_seduc_dao = EmployeSeducDAO()
    #     if not employe_seduc_id:
    #         return None
    #     with EmployeSeducDAO() as employe_seduc_dao:
    #         employe_seduc_entity = employe_seduc_dao.find_by_id(employe_seduc_id)
    #         return employe_seduc_entity
        

    
    # def employe_seduc(self, session=None, commit_on_exit=True, close_on_exit=True):
    #     """
    #     Finds the associated employes in the database
    #     """
    #     if hasattr(self, '_employes'):
    #         return self._employes

    #     if not self.id():
    #         raise Exception("You need an id to get dependencies")

    #     with OrderDAO(session, commit_on_exit, close_on_exit) as dao:
    #         # Obtain the entity of this model
    #         entity = dao._find_entity_by_id(self.id())

    #         # Finds the associated entities
    #         associated_entities = entity.employe_seduc_id

    #         # Use the factory to get a manager of the associated entities
    #         employe_seduc_dao = EmployeSeducDAOFactory.create(dao.session())

    #         # A list of the models of the associated entities
    #         # # Esse método transforma uma Entity em um Model. Isso é importante porque não podemos deixar um Entity ir pra camada de Negócios
    #         self._employes = [employe_seduc_dao._build_model_from_entity(e) for e in associated_entities]
    #     return self._employe_seduc_id

    # def transporter(self, session=None, commit_on_exit=True, close_on_exit=True):
    #     """
    #     Finds the associated transporters in the database
    #     """
    #     if hasattr(self, '_transporters'):
    #         return self._transporter_id

    #     if not self.id():
    #         raise Exception("You need an id to get dependencies")

    #     with OrderDAO(session, commit_on_exit, close_on_exit) as dao:
    #         # Obtain the entity of this model
    #         entity = dao._find_entity_by_id(self.id())

    #         # Finds the associated entities
    #         associated_entities = entity.transporter_id

    #         # Use the factory to get a manager of the associated entities
    #         transporter_id_dao = TransporterDAOFactory.create(dao.session())

    #         # A list of the models of the associated entities
    #         self._transporters = [transporter_id_dao._build_model_from_entity(e) for e in associated_entities]
    #     return self._transporter_id
    
    # def school(self, session=None, commit_on_exit=True, close_on_exit=True):
    #     """
    #     Finds the associated school in the database
    #     """
    #     if hasattr(self, '_school'):
    #         return self._school_id

    #     if not self.id():
    #         raise Exception("You need an id to get dependencies")

    #     with OrderDAO(session, commit_on_exit, close_on_exit) as dao:
    #         # Obtain the entity of this model
    #         entity = dao._find_entity_by_id(self.id())

    #         # Finds the associated entities
    #         associated_entities = entity.school_id

    #         # Use the factory to get a manager of the associated entities
    #         school_id_dao = SchoolDAOFactory.create(dao.session())

    #         # A list of the models of the associated entities
    #         self._school = [school_id_dao._build_model_from_entity(e) for e in associated_entities]
    #     return self._school
    
    # def supplier(self, session=None, commit_on_exit=True, close_on_exit=True):
    #     """
    #     Finds the associated supplier in the database
    #     """
    #     if hasattr(self, '_supplier'):
    #         return self._supplier_id

    #     if not self.id():
    #         raise Exception("You need an id to get dependencies")

    #     with OrderDAO(session, commit_on_exit, close_on_exit) as dao:
    #         # Obtain the entity of this model
    #         entity = dao._find_entity_by_id(self.id())

    #         # Finds the associated entities
    #         associated_entities = entity.supplier_id

    #         # Use the factory to get a manager of the associated entities
    #         supplier_id_dao = SupplierDAOFactory.create(dao.session())

    #         # A list of the models of the associated entities
    #         self._supplier = [supplier_id_dao._build_model_from_entity(e) for e in associated_entities]
    #     return self._supplier