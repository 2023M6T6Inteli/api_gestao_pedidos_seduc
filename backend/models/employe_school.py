import json

from .factories import *
from .dao import BaseDAO
from models.entities import *

""" DAO
================================================================================
"""
# EmployeSchoolDAO terá todas as funcionalidades de BaseDAO, como gerenciamento de sessões de banco de dados.
class EmployeSchoolDAO(BaseDAO):

    def create_employe_school(self, map_):
        # Cria uma entidade estudante
        employe_school_entity = EmployeSchoolEntity(
            name = map_['name'],
            cpf = map_['cpf'],
            email = map_['email'],
            password = map_['password'],
            school_id = map_['school_id'],
        )

        # Adiciona a sessão para que seja inserido ao banco de daos
        return self._session.add(employe_school_entity)
    
    def update_employe_school(self, id, map_):
        entity = self._find_entity_by_id(id)
        if entity:
            for key, value in map_.items():
                setattr(entity, key, value)
            return self._build_model_from_entity(entity)
        else:
            return None
        
    def delete_employe_school(self, id):
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
        return self._session.query(EmployeSchoolEntity).all()

    def _find_entity_by_id(self, id):
        return self._session.query(EmployeSchoolEntity).filter(EmployeSchoolEntity.id == id).first()

    def _find_entity_by_cpf(self, cpf):
        return self._session.query(EmployeSchoolEntity).filter(EmployeSchoolEntity.cpf == cpf).first()

    def _build_model_from_entity(self, entity):
        """
        Build a EmployeSchool model out of an entity
        """
        employe_school = EmployeSchool(
            id = entity.id,
            name = entity.name,
            cpf = entity.cpf,
            email = entity.email,
            password = entity.password,
            school_id = entity.school_id,
        )
        return employe_school
    
    def _build_models_from_entities(self, entities):
        """
        Build a list of EmployeSchool models out of a list of entities
        """
        employe_schools = []
        for entity in entities:
            employe_schools.append(self._build_model_from_entity(entity))
        return employe_schools

    def _map_to_school_entities(self, school_ids):
        """
        Converts the courses ids in the map to their entities
        """
        mng = SchoolDAOFactory.create(self.session())
        entities = []
        for id in school_ids:
            entity = mng._find_entity_by_id(id)
            entities.append(entity)
        return entities
    
    def _find_school_entity_by_id(self, id):
        school_dao = SchoolDAOFactory.create(self.session())
        return school_dao._find_entity_by_id(id)


""" Model
================================================================================
"""
# Esta classe representa o modelo de um estudante em seu sistema. Ela possui atributos como id, ra, name e courses, além de métodos para 
# manipular esses atributos e para converter os dados do estudante em diferentes formatos, como um dicionário ou JSON.

# O modelo EmployeSchool é uma representação mais amigável e prática dos dados de um estudante, que pode ser usada em outras partes do seu 
# aplicativo, como interfaces de usuário, lógica de negócios ou comunicação entre diferentes componentes do sistema.
class EmployeSchool:

    def __init__(self, id, name, cpf, email, password, school_id):
            self._id = id
            self._name = name
            self._cpf = cpf
            self._email = email
            self._password = password
            self._school_id = school_id

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
    def school_id(self):
        return self._school_id
    
    def add_school_id(self, school_id):
        self._school_id = school_id

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
        return {
            "id": self._id,
            "name": self._name,
            "cpf": self._cpf,
            "email": self._email,
            "password": self._password,
            "school_id": self._school_id,
        }
    
    def schools(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Finds the associated models in the database
        """
        if (self._schools):
            return self._schools

        if (not self.id()):
            raise Exception("You need an id to get dependencies")

        with EmployeSchoolDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.schools

            # Use the factory to get a manager of the associated entities
            school_dao = SchoolDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            self._schools = [school_dao._build_model_from_entity(e) for e in associated_entities]
        return self._schools