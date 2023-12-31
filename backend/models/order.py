
"""
Classes e Seus Papéis
OrderDAO (Data Access Object):

Papel: Interage diretamente com o banco de dados. Possui métodos para criar, atualizar, deletar e buscar pedidos (orders).
Funcionamento: Cada método manipula a entidade OrderEntity, que representa a tabela de pedidos no banco de dados. Por exemplo, create_order cria um novo pedido, find_by_id busca um pedido pelo ID, etc.
OrderEntity:

Papel: Representa a estrutura de dados da tabela de pedidos no banco de dados.
Funcionamento: Define as colunas da tabela como atributos da classe. Cada instância de OrderEntity corresponde a uma linha na tabela de pedidos.
Order:

Papel: Representa um modelo de negócio de pedido, usado na lógica da aplicação.
Funcionamento: Armazena informações de um pedido e pode incluir métodos para processamento de negócios ou transformação de dados (como conversão para JSON).
SupplierDAO, SchoolDAO, TransporterDAO, EmployeSeducDAO:

Papel: Semelhante ao OrderDAO, mas para outras entidades como fornecedores, escolas, transportadoras e funcionários da SEDUC.
Funcionamento: Cada DAO gerencia operações de banco de dados para sua respectiva entidade.
Interações Entre Classes
Quando OrderDAO precisa de informações sobre fornecedores, escolas, transportadoras ou funcionários da SEDUC, ele usa os respectivos DAOs. Por exemplo, get_supplier em OrderDAO usa SupplierDAO para buscar informações de um fornecedor.

Os métodos em OrderDAO, como create_order ou find_by_id, criam ou recuperam instâncias de OrderEntity do banco de dados. Eles então podem construir um modelo Order a partir destas entidades para uso na lógica de negócios da aplicação.

Papel dos Getters e Setters
Getters: São métodos usados para obter o valor de um atributo de um objeto. Por exemplo, order.id() é um getter que retorna o ID do pedido.
Setters: São métodos usados para definir ou atualizar o valor de um atributo. Por exemplo, order.add_id(123) é um setter que define o ID do pedido como 123.
Imagine que você tem uma caixa (objeto) com itens dentro (atributos). Um getter é como perguntar "O que está dentro da caixa?". Um setter é como dizer "Coloque este item na caixa".

Simplificando com Exemplo
Criação de um Pedido:

O usuário da aplicação decide criar um novo pedido.
A aplicação recebe os dados do pedido e os passa para OrderDAO.create_order.
OrderDAO cria uma nova instância de OrderEntity com esses dados e a salva no banco de dados.
Busca de um Pedido:

O usuário quer ver detalhes de um pedido específico.
A aplicação pede a OrderDAO para encontrar o pedido pelo ID usando find_by_id.
OrderDAO recupera a OrderEntity correspondente do banco de dados.
OrderDAO constrói um modelo Order a partir da entidade e retorna para a aplicação, talvez após convertê-lo para JSON.
Cada classe e método tem um papel específico, trabalhando juntos para gerenciar a lógica de negócios e interações com o banco de dados.
"""
import json
import logging

from flask import jsonify
from models.employe_seduc import EmployeSeducDAO
from models.school import SchoolDAO
from models.transporter import TransporterDAO

from models.supplier import SupplierDAO

from .factories import *
from .dao import BaseDAO
from models.entities import *
from sqlalchemy.orm import joinedload
# from models.entities import StatusComponenteConfirmarEntregaEntity

""" DAO
================================================================================
"""


# class StatusComponenteConfirmarEntegaDAO(BaseDAO):
#     def iniciando_status(self,status):
#         entity = StatusComponenteConfirmarEntregaEntity(
#             status = status
#         )
#         return self._session.add(entity)
    
#     def update_status(self, status):
#         entity = self._session.query(StatusComponenteConfirmarEntregaEntity).first()
#         if entity:
#             setattr(entity, 'status', status)
#             return jsonify({"status": "ok"})

class OrderDAO(BaseDAO):

    def create_order(self, map_):
        """
        Add a order to the Database
        """

        if isinstance(map_['school_id'], str):
                with SchoolDAO() as school_dao:
                    school_id = school_dao.get_school_id_by_name(map_['school_id'])
                    map_['school_id'] = school_id

        if isinstance(map_['transporter_id'], str):
            with TransporterDAO() as transporter_dao:
                transporter_id = transporter_dao.get_transporter_id_by_name(map_['transporter_id'])
                map_['transporter_id'] = transporter_id

        if isinstance(map_['supplier_id'], str):
            with SupplierDAO() as supplier_dao:
                supplier_id = supplier_dao.get_supplier_id_by_name(map_['supplier_id'])
                map_['supplier_id'] = supplier_id
        
        entity = OrderEntity(
            nf = map_['nf'],
            nr =map_['nr'],
            purchase_date = map_['purchase_date'],
            delivery_date = map_.get('delivery_date'),
            status = OrderStatus(map_['status']),
            amount = map_['amount'],
            school_id = map_['school_id'],
            supplier_id = map_['supplier_id'],
            employe_seduc_id = map_['employe_seduc_id'],
            transporter_id = map_.get('transporter_id')
        )
        return self._session.add(entity)
    
    # def create_order_by_name_of_entities(self, map_):
    #     supplier_dao = SupplierDAO()
    #     transpoerter_dao = TransporterDAO()
    #     school_dao = SchoolDAO()

    #     if not school_id:
    #         return None
    #     with SchoolDAO() as school_dao:
    #         school_id = school_dao.get_school_id_by_name(map_['school_name'])
    #         map_['school_id'] = school_id
    #         return school_id
        

    #     entity = OrderEntity(
    #             nf = map_['nf'],
    #             nr =map_['nr'],
    #             purchase_date = map_['purchase_date'],
    #             delivery_date = map_.get('delivery_date'),
    #             status = OrderStatus(map_['status']),
    #             amount = map_['amount'],
    #             school_id = map_['school_id'],
    #             supplier_id = map_['supplier_id'],
    #             employe_seduc_id = map_['employe_seduc_id'],
    #             transporter_id = map_.get('transporter_id')
    #     )
    #     return self._session.add(entity)
    
    def create_orders(self, orders_data):
        orders_entities = []
        for map_ in orders_data:
            entity = OrderEntity(
                nf = map_['nf'],
                nr =map_['nr'],
                purchase_date = map_['purchase_date'],
                delivery_date = map_.get('delivery_date'),
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
        logging.error(f"entrou find_all dao")
        entities = self.find_all_entity()
        return self._build_models_from_entities(entities)


    def find_by_id(self, id):
        """
        Finds an instance by id
        """
        entity = self._find_entity_by_id(id)
        if (entity):
            logging.debug("construindo models.")
            return self._build_model_from_entity(entity)
        

    def find_by_nr(self, nr):
        """
        Finds an instance by nr
        """
        entity = self._session.query(OrderEntity).filter(OrderEntity.nr == nr).first()
        if (entity):
            return self._build_model_from_entity(entity)
    

##############################################################################################################

 ###### PREENCHIMENTO DA PÁGINAS DE PEDIDOS E HISTÓRICO DE PEDIDOS ######

##############################################################################################################

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
        
    def get_supplier_model(self, entity):
        supplier_dao = SupplierDAO()
        with SupplierDAO() as supplier_dao:
            supplier_model = supplier_dao._build_model_from_entity(entity)
            return supplier_model
        
    def get_transporter_model(self, entity):
        transporter_dao = TransporterDAO()
        with TransporterDAO() as transporter_dao:
            transporter_model = transporter_dao._build_model_from_entity(entity)
            return transporter_model
        
    def get_school_model(self, entity):
        # school = entity.school_id
        school_dao = SchoolDAO()
        with SchoolDAO() as school_dao:
            school_model = school_dao._build_model_from_entity(entity)
            return school_model
        
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
        try:
            logging.debug("entrou find_All_entity na model order.")
            return self._session.query(OrderEntity).all()
        except Exception as e:
            logging.error(f"Erro na model find_all_entity order: {e}")
            raise e

    
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
        logging.error(f"entrou build model.", entity)

        supplier = self.get_supplier_model(entity.supplier)
        school = self.get_school_model(entity.school)
        transporter = self.get_transporter_model(entity.transporter)




        order = Order(
            id = entity.id,
            nf = entity.nf,
            nr = entity.nr,
            purchase_date = entity.purchase_date,
            delivery_date = entity.delivery_date,
            status = entity.status,
            amount = entity.amount,
            supplier=supplier,
            school=school,
            transporter=transporter,            
            employe_seduc_id = entity.employe_seduc_id
        )
        logging.error(f"construiu model.")
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
    


""" Model
================================================================================
"""

class Order:

    def __init__(self, id, nf, nr, purchase_date, delivery_date, status, amount, supplier, school, transporter, employe_seduc_id):
        self._id = id
        self._nf = nf
        self._nr = nr
        self._purchase_date = purchase_date
        self._delivery_date = delivery_date
        self._status = status
        self._amount = amount
        self._supplier = supplier
        self._school = school
        self._transporter = transporter
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
    
    def purchase_date(self):
        return self._purchase_date
    
    def add_purchase_date(self, purchase_date):
        self._purchase_date = purchase_date

    def delivery_date(self):
        return self._delivery_date
    
    def add_delivery_date(self, delivery_date):
        self._delivery_date = delivery_date
    
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
            elif isinstance(value, str):
                map_[key] = value.encode('utf-8').decode('utf-8')
        return json.dumps(map_, indent=indent, ensure_ascii=False)

    def to_map(self):
        logging.error(f"entrou no map")
        supplier_map = self._supplier.to_map() if self._supplier else None
        school_map = self._school.to_map() if self._school else None
        transporter_map = self._transporter.to_map() if self._transporter else None



        return {
            "id": self.id(),
            "nf": self.nf(),
            "nr": self.nr(),
            "purchase_date": self.purchase_date(),
            "delivery_date": self.delivery_date(),
            "status": self.status().to_dict(),
            "amount": self.amount(),
            "supplier": supplier_map,
            "school": school_map,
            "transporter": transporter_map,
            "employe_seduc_id": self.employe_seduc_id()
        }
    
