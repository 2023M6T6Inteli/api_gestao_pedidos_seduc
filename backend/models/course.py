import json

from .factories import *
from .dao import BaseDAO
from models.entities import *

""" DAO
================================================================================
"""

class CourseDAO(BaseDAO):

    def create_course(self, map_):
        """
        Add a course to the Database
        """
        entity = CourseEntity(
            code = map_['code'],
            name = map_['name']
        )
        return self._session.add(entity)

    def find_by_id(self, id):
        """
        Finds an instance by id
        """
        entity = self._find_entity_by_id(id)
        if (entity):
            return self._build_model_from_entity(entity)

    def find_by_code(self, code):
        """
        Finds an instance by code
        """
        entity = self._session.query(CourseEntity).filter(CourseEntity.code == code).first()
        if (entity):
            return self._build_model_from_entity(entity)

    # Private methods
    # -------------------------------------------------------------------------

    def _find_entity_by_id(self, id):
        return self._session.query(CourseEntity).filter(CourseEntity.id == id).first()

    def _build_model_from_entity(self, entity):
        """
        Build a Student model out of an entity
        """
        course = Course(
            id = entity.id,
            code = entity.code,
            name = entity.name
        )
        return course

""" Model
================================================================================
"""

class Course:

    def __init__(self, id, code, name):
        self._id = id
        self._code = code
        self._name = name
        self._students = None

    def id(self):
        return self._id

    def add_id(self):
        self._id = id

    def name(self):
        return self._name

    def add_name(self, name):
        self._name = name

    def code(self):
        return self._code

    def add_code(self, code):
        self._code = code

    def jsonify(self, indent=2):
        map_ = self.to_map()
        return json.dumps(map_, indent=indent)

    def to_map(self):
        return {
            "id": self.id(),
            "code": self.code(),
            "name": self.name()
        }
    
    def students(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Finds the associated models in the database
        """
        if (self._students):
            return self._students

        if (not self.id()):
            raise Exception("You need an id to get dependencies")

        with CourseDAO(session, commit_on_exit, close_on_exit) as dao:
            # Obtain the entity of this model
            entity = dao._find_entity_by_id(self.id())

            # Finds the associated entities
            associated_entities = entity.students

            # Use the factory to get a manager of the associated entities
            student_dao = StudentDAOFactory.create(dao.session())

            # A list of the models of the associated entities
            self._students = [student_dao._build_model_from_entity(e) for e in associated_entities]
        return self._students
