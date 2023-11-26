import logging
from models import employe_seduc


class EmployeSeducServices:

    def create_employe_seduc(employe_seduc_map):
        try:
            with employe_seduc.EmployeSeducDAO() as dao:
                dao.create_employe_seduc(employe_seduc_map)
            return True
        except (ValueError, TypeError) as e:
            logging.error(f"Erro de dados ao criar empregado: {e}")
            return False
        except Exception as e:
            logging.error(f"Erro inesperado ao criar empregado: {e}")
            return False

    def update_employe_seduc(id, employe_seduc_map):
        try:
            with employe_seduc.EmployeSeducDAO() as dao:
                dao.update_employe_seduc(id, employe_seduc_map)
            return True
        except (ValueError, TypeError) as e:
            logging.error(f"Erro de dados ao atualizar empregado: {e}")
            return False
        except Exception as e:
            logging.error(f"Erro inesperado ao atualizar empregado: {e}")
            return False

    def delete_employe_seduc(id):
        try:
            with employe_seduc.EmployeSeducDAO() as dao:
                dao.delete_employe_seduc(id)
            return True
        except Exception as e:
            logging.error(f"Erro ao deletar empregado: {e}")
            return False

    def find_all(self):
        try:
            with employe_seduc.EmployeSeducDAO() as dao:
                result = dao.find_all()
            return result
        except Exception as e:
            logging.error(f"Erro ao buscar todos os empregados: {e}")
            return []

    def find_by_id(self, id):
        try:
            with employe_seduc.EmployeSeducDAO() as dao:
                return dao.find_by_id(id)
        except Exception as e:
            logging.error(f"Erro ao buscar empregado por id: {e}")
            return None

    def find_by_cpf(self, cpf):
        try:
            with employe_seduc.EmployeSeducDAO() as dao:
                return dao.find_by_cpf(cpf)
        except Exception as e:
            logging.error(f"Erro ao buscar empregado por cpf: {e}")
            return None
        