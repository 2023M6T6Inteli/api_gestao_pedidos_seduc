import logging
from models import school


class SchoolServices:

    def create_school(school_map):
        try:
            with school.SchoolDAO() as dao:
                logging.error(f"dados recebidos: {school_map}")
                dao.create_school(school_map)
                logging.error(f"dadoa recebidos: {school_map}")
            return True
        except (ValueError, TypeError) as e:
            logging.error(f"Erro de dados ao criar school: {e}")
            return False
        except Exception as e:
            logging.error(f"Erro inesperado SchoolService ao criar school: {e}")
            return False
        
    def create_schools(schools_data):
        try:
            with school.SchoolDAO() as dao:
                dao.create_schools(schools_data)
            return True
        except (ValueError, TypeError) as e:
            logging.error(f"Erro de dados ao criar school: {e}")
            return False
        except Exception as e:
            logging.error(f"Erro inesperado ao criar schools: {e}")
            return False

    def update_school(id, school_map):
        try:
            with school.SchoolDAO() as dao:
                dao.update_school(id, school_map)
            return True
        except (ValueError, TypeError) as e:
            logging.error(f"Erro de dados ao atualizar school: {e}")
            return False
        except Exception as e:
            logging.error(f"Erro inesperado ao atualizar school: {e}")
            return False

    def delete_school(id):
        try:
            with school.SchoolDAO() as dao:
                dao.delete_school(id)
            return True
        except Exception as e:
            logging.error(f"Erro ao deletar school: {e}")
            return False
        
    def delete_all_schools():
        try:
            with school.SchoolDAO() as dao:
                dao.delete_all_schools()
            return True
        except Exception as e:
            logging.error(f"Erro ao deletar todas as escolas: {e}")
            return False

    def find_all(self):
        try:
            with school.SchoolDAO() as dao:
                result = dao.find_all()
            return result
        except Exception as e:
            logging.error(f"Erro ao buscar todos os schools: {e}")
            return []

    def find_by_id(self, id):
        try:
            with school.SchoolDAO() as dao:
                return dao.find_by_id(id)
        except Exception as e:
            logging.error(f"Erro ao buscar school por id: {e}")
            return None

    def find_by_cnpj(self, cnpj):
        try:
            with school.SchoolDAO() as dao:
                return dao.find_by_cnpj(cnpj)
        except Exception as e:
            logging.error(f"Erro ao buscar school por cnpj: {e}")
            return None
        