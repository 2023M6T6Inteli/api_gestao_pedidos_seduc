
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
from models.employe_seduc import EmployeSeducDAO
from models.school import SchoolDAO
from models.transporter import TransporterDAO

from models.supplier import SupplierDAO

from .factories import *
from .dao import BaseDAO
from models.entities import *
from sqlalchemy.orm import joinedload

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
        
    # def find_all(self):
    #     entities = self.find_all_entity()
    #     return self._build_models_from_entities(entities)

    def find_all(self):
        try:
            logging.debug("entrou find_All na model orderDAO.")
            explain_output, entities = self.find_all_entity()  # Desempacotando os dois retornos
            logging.debug("passou entities e explain na model orderDAO.")
            return self._build_models_from_entities(entities), explain_output
        except Exception as e:
            logging.error(f"Erro na model find_all orderDAO: {e}")
            raise e

    def find_by_id(self, id):
        """
        Finds an instance by id
        """
        entity = self._find_entity_by_id(id)
        if (entity):
            logging.debug("construindo models.")
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


        
    # def _find_entity_by_id(self, id):
    #     return self._session.query(OrderEntity).filter(OrderEntity.id == id).first()
    def _find_entity_by_id(self, id):
        try:
            logging.debug("entrou find_All_entity na model order.")
            # Cria a consulta SQLAlchemy
            query = self._session.query(OrderEntity).filter(OrderEntity.id == id)
            logging.debug("passou query na model order.")
            # Obtém a representação em string da consulta com EXPLAIN
            explain_query = str(query.statement.compile(dialect=self._session.bind.dialect, compile_kwargs={"literal_binds": True}))
            logging.error(f"explain_query: {explain_query}")
            # Executar EXPLAIN na consulta
            # explain_result = self._session.execute(f"EXPLAIN {explain_query}")
            # logging.error(f"explain_result: {explain_result}")
            # Criar uma lista para armazenar os resultados do EXPLAIN
            # explain_output = []
            # # Iterar sobre os resultados do EXPLAIN e adicioná-los à lista
            # for row in explain_result:
            #     explain_output.append(row)
            # # Executar a consulta original e retornar os resultados do EXPLAIN para análise
            result = query.first()
            if result:
                logging.info(f"Entidade encontrada com ID {id}")
            else:
                logging.warning(f"Nenhuma entidade encontrada com ID {id}")
            # logging.error(f"explain_output: {explain_output}")
            # Se você quiser retornar também os resultados da consulta original,
            # descomente a linha abaixo e ajuste conforme necessário.
            return result
        except Exception as e:
            logging.error(f"Erro na model find_all_entity order: {e}")
            raise e
    
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
    # def find_all_entity(self):
    #     return self._session.query(OrderEntity).all()

    # def find_all_entity(self):
    #     return self._session.query(OrderEntity)\
    #         .filter(OrderEntity.id == id)\
    #         .options(joinedload(OrderEntity.supplier))\
    #         .options(joinedload(OrderEntity.school))\
    #         .options(joinedload(OrderEntity.transporter))\
    #         .first()
    #     # return self._session.query(OrderEntity).all()

    def find_all_entity(self):
        try:
            logging.debug("entrou find_All_entity na model order.")
            # Cria a consulta SQLAlchemy
            query = self._session.query(OrderEntity)
            logging.debug("passou query na model order.")
            logging.error(f"query: {query}")

            # Converte a consulta SQLAlchemy em uma string SQL
            sql = str(query.statement.compile(dialect=self._session.bind.dialect))

            logging.error(f"sql: {sql}")


            # Executar EXPLAIN na consulta
            explain_result = self._session.execute(f"EXPLAIN {sql}")

            logging.error(f"explain_result: {explain_result}")

            # Criar uma lista para armazenar os resultados do EXPLAIN
            explain_output = []

            

            # Iterar sobre os resultados do EXPLAIN e adicioná-los à lista
            for row in explain_result:
                explain_output.append(row)

            # Retorna os resultados do EXPLAIN para análise
            # return explain_output
            logging.error(f"explain_output: {explain_output}")
            # Se você quiser retornar também os resultados da consulta original,
            # descomente a linha abaixo e ajuste conforme necessário.
            return explain_output, query.all()
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
        logging.error(f"começou queries supplier, transporter...")
        supplier = self.get_supplier(entity.supplier_id)
        school = self.get_school(entity.school_id)
        transporter = self.get_transporter(entity.transporter_id)
        logging.error(f"passou queries supplier, transporter...")
        order = Order(
            id = entity.id,
            nf = entity.nf,
            nr = entity.nr,
            purchase_date = entity.purchase_date,
            delivery_date = entity.delivery_date,
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