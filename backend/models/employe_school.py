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
        """
        Add a employe_school to the Database
        """
        # Cria uma entidade estudante
        employe_school_entity = EmployeSchoolEntity(
            id = map_['id'],
            name = map_['name'],
            cpf = map_['cpf'],
            email = map_['email'],
            password = map_['password'],
            school_id = map_['school_id'],
        )

        # Adiciona os cursos
        school_id = int(map_["school_id"])
        school_entity = self._find_school_entity_by_id(school_id)
        employe_school_entity.schools = [school_entity]

        # Adiciona a sessão para que seja inserido ao banco de daos
        return self._session.add(employe_school_entity)
    
    def update_employe_school(self, map_):
        """
        Update a employe_school to the Database
        """
        entity = self._find_entity_by_id(id)
        if entity:
            for key, value in map_.items():
                setattr(entity, key, value)
                self._session.commit()
            return self._build_model_from_entity(entity)
        else:
            return None
        
    def delete_employe_school(self, id):
        """
        Delete a employe_school to the Database
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
            self.name = name
            self.cpf = cpf
            self.email = email
            self.password = password
            self.school_id = school_id


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

    def school_id(self):
        return self._school_id
    
    def add_school_id(self, school_id):
        self._school_id = school_id

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
            "school_id": self.school_id(),
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