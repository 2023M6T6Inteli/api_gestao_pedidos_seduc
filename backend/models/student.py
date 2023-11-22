import json

from .factories import *
from .dao import BaseDAO
from models.entities import *

""" DAO
================================================================================
"""
# StudentDAO terá todas as funcionalidades de BaseDAO, como gerenciamento de sessões de banco de dados.
class StudentDAO(BaseDAO):

    def create_student(self, map_):
        """
        Add a student to the Database
        """
        # Cria uma entidade estudante
        student_entity = StudentEntity(
            ra = map_['ra'],
            name = map_['name']
        )

        # Adiciona os cursos
        course_id = int(map_["course_id"])
        course_entity = self._find_course_entity_by_id(course_id)
        student_entity.courses = [course_entity]

        # Adiciona a sessão para que seja inserido ao banco de daos
        return self._session.add(student_entity)

    def find_by_id(self, id):
        """
        Finds an instance by id
        """
        entity = self._find_entity_by_id(id)
        if (entity):
            return self._build_model_from_entity(entity)

    def find_by_ra(self, ra):
        """
        Finds an instance by ra
        """
        entity = self._find_entity_by_ra(ra)
        if (entity):
            return self._build_model_from_entity(entity)

    # Private methods
    # -------------------------------------------------------------------------

    def _find_entity_by_id(self, id):
        return self._session.query(StudentEntity).filter(StudentEntity.id == id).first()

    def _find_entity_by_ra(self, ra):
        return self._session.query(StudentEntity).filter(StudentEntity.ra == ra).first()

    def _build_model_from_entity(self, entity):
        """
        Build a Student model out of an entity
        """
        student = Student(
            id = entity.id,
            ra = entity.ra,
            name = entity.name
        )
        return student

    def _map_to_courses_entities(self, course_ids):
        """
        Converts the courses ids in the map to their entities
        """
        mng = CourseDAOFactory.create(self.session())
        entities = []
        for id in course_ids:
            entity = mng._find_entity_by_id(id)
            entities.append(entity)
        return entities
    
    def _find_course_entity_by_id(self, id):
        course_dao = CourseDAOFactory.create(self.session())
        return course_dao._find_entity_by_id(id)


""" Model
================================================================================
"""
# Esta classe representa o modelo de um estudante em seu sistema. Ela possui atributos como id, ra, name e courses, além de métodos para 
# manipular esses atributos e para converter os dados do estudante em diferentes formatos, como um dicionário ou JSON.

# O modelo Student é uma representação mais amigável e prática dos dados de um estudante, que pode ser usada em outras partes do seu 
# aplicativo, como interfaces de usuário, lógica de negócios ou comunicação entre diferentes componentes do sistema.
class Student:

    def __init__(self, id, ra, name):
        self._id = id
        self._ra = ra
        self._name = name
        self._courses = None

    def id(self):
        return self._id

    def add_id(self):
        self._id = id

    def name(self):
        return self._name

    def add_name(self, name):
        self._name = name

    def ra(self):
        return self._ra

    def add_ra(self, ra):
        self._ra = ra

    def jsonify(self, indent=2):
        map_ = self.to_map()
        return json.dumps(map_, indent=indent)

    def to_map(self):
        return {
            "id": self.id(),
            "ra": self.ra(),
            "name": self.name()
        }
    
    def courses(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Finds the associated models in the database
        """
        if (self._courses):
            return self._courses

        if (not self.id()):
            raise Exception("You need an id to get dependencies")

        with StudentDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.courses

            # Use the factory to get a manager of the associated entities
            course_dao = CourseDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            self._courses = [course_dao._build_model_from_entity(e) for e in associated_entities]
        return self._courses