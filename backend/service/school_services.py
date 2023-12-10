import logging
from models import school


class SchoolServices:

    def create_school(school_map):
        try:
            with school.SchoolDAO() as dao:
                dao.create_school(school_map)
            return True
        except (ValueError, TypeError) as e:
            return False
        except Exception as e:
            return False
        
    def create_schools(schools_data):
        try:
            with school.SchoolDAO() as dao:
                dao.create_schools(schools_data)
            return True
        except (ValueError, TypeError) as e:
            return False
        except Exception as e:
            return False

    def update_school(id, school_map):
        try:
            with school.SchoolDAO() as dao:
                dao.update_school(id, school_map)
            return True
        except (ValueError, TypeError) as e:
            return False
        except Exception as e:
            return False

    def delete_school(id):
        try:
            with school.SchoolDAO() as dao:
                dao.delete_school(id)
            return True
        except Exception as e:
            return False
        
    def delete_all_schools():
        try:
            with school.SchoolDAO() as dao:
                dao.delete_all_schools()
            return True
        except Exception as e:
            return False

    def find_all(self):
        try:
            with school.SchoolDAO() as dao:
                result = dao.find_all()
            return result
        except Exception as e:
            return []

    def find_by_id(self, id):
        try:
            with school.SchoolDAO() as dao:
                return dao.find_by_id(id)
        except Exception as e:
            return None

    def find_by_cnpj(self, cnpj):
        try:
            with school.SchoolDAO() as dao:
                return dao.find_by_cnpj(cnpj)
        except Exception as e:
            return None
        