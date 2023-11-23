import json

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
            id = map_['id'],
            name = map_['name'],
            cpf = map_['cpf'],
            email = map_['email'],
            password = map_['password'],
            transporter_id = map_['transporter_id'],
        )

        # Adiciona os cursos
        transporter_id = int(map_["transporter_id"])
        transporter_entity = self._find_transporter_entity_by_id(transporter_id)
        employe_transporter_entity.transporters = [transporter_entity]

        # Adiciona a sessão para que seja inserido ao banco de daos
        return self._session.add(employe_transporter_entity)

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
            transporter_id = entity.transporter_id,
        )
        return employe_transporter

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

    def __init__(self, id, name, cpf, email, password, transporter_id):
            self._id = id
            self.name = name
            self.cpf = cpf
            self.email = email
            self.password = password
            self.transporter_id = transporter_id


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

    def transporter_id(self):
        return self._transporter_id

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
            "transporter_id": self.transporter_id(),
        }
    
    def transporters(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Finds the associated models in the database
        """
        if (self._transporters):
            return self._transporters

        if (not self.id()):
            raise Exception("You need an id to get dependencies")

        with EmployeTransporterDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.transporters

            # Use the factory to get a manager of the associated entities
            transporter_dao = TransporterDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            self._transporters = [transporter_dao._build_model_from_entity(e) for e in associated_entities]
        return self._transporters