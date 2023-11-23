import jsoncour

from .factories import *
from .dao import BaseDAO
from models.entities import *

""" DAO
================================================================================
"""
# EmployeSupplierDAO terá todas as funcionalidades de BaseDAO, como gerenciamento de sessões de banco de dados.
class EmployeSupplierDAO(BaseDAO):

    def create_employe_supplier(self, map_):
        """
        Add a employe_supplier to the Database
        """
        # Cria uma entidade estudante
        employe_supplier_entity = EmployeSupplierEntity(
            id = map_['id'],
            name = map_['name'],
            cpf = map_['cpf'],
            email = map_['email'],
            password = map_['password'],
            supplier_id = map_['supplier_id'],
        )

        # Adiciona os cursos
        supplier_id = int(map_["supplier_id"])
        supplier_entity = self._find_supplier_entity_by_id(supplier_id)
        employe_supplier_entity.suppliers = [supplier_entity]

        # Adiciona a sessão para que seja inserido ao banco de daos
        return self._session.add(employe_supplier_entity)
    
    def update_employe_supplier(self, map_):
        """
        Update a employe_supplier to the Database
        """
        entity = self._find_entity_by_id(id)
        if entity:
            for key, value in map_.items():
                setattr(entity, key, value)
                self._session.commit()
            return self._build_model_from_entity(entity)
        else:
            return None
    
    def delete_employe_supplier(self, id):
        """
        Delete a employe_supplier to the Database
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
        return self._session.query(EmployeSupplierEntity).filter(EmployeSupplierEntity.id == id).first()

    def _find_entity_by_cpf(self, cpf):
        return self._session.query(EmployeSupplierEntity).filter(EmployeSupplierEntity.cpf == cpf).first()

    def _build_model_from_entity(self, entity):
        """
        Build a EmployeSupplier model out of an entity
        """
        employe_supplier = EmployeSupplier(
            id = entity.id,
            name = entity.name,
            cpf = entity.cpf,
            email = entity.email,
            password = entity.password,
            supplier_id = entity.supplier_id,
        )
        return employe_supplier

    def _map_to_supplier_entities(self, supplier_ids):
        """
        Converts the courses ids in the map to their entities
        """
        mng = SupplierDAOFactory.create(self.session())
        entities = []
        for id in supplier_ids:
            entity = mng._find_entity_by_id(id)
            entities.append(entity)
        return entities
    
    def _find_supplier_entity_by_id(self, id):
        supplier_dao = SupplierDAOFactory.create(self.session())
        return supplier_dao._find_entity_by_id(id)


""" Model
================================================================================
"""
# Esta classe representa o modelo de um estudante em seu sistema. Ela possui atributos como id, ra, name e courses, além de métodos para 
# manipular esses atributos e para converter os dados do estudante em diferentes formatos, como um dicionário ou JSON.

# O modelo EmployeSupplier é uma representação mais amigável e prática dos dados de um estudante, que pode ser usada em outras partes do seu 
# aplicativo, como interfaces de usuário, lógica de negócios ou comunicação entre diferentes componentes do sistema.
class EmployeSupplier:

    def __init__(self, id, name, cpf, email, password, supplier_id):
            self._id = id
            self.name = name
            self.cpf = cpf
            self.email = email
            self.password = password
            self.supplier_id = supplier_id


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

    def supplier_id(self):
        return self._supplier_id

    def add_supplier_id(self, supplier_id):
        self._supplier_id = supplier_id

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
            "supplier_id": self.supplier_id(),
        }
    
    def suppliers(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Finds the associated models in the database
        """
        if (self._suppliers):
            return self._suppliers

        if (not self.id()):
            raise Exception("You need an id to get dependencies")

        with EmployeSupplierDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.suppliers

            # Use the factory to get a manager of the associated entities
            supplier_dao = SupplierDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            self._suppliers = [supplier_dao._build_model_from_entity(e) for e in associated_entities]
        return self._suppliers