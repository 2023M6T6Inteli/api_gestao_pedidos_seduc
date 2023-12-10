import logging
from models import order
from models import employe_seduc


class EmployeSeducServices:

    def create_employe_seduc(employe_seduc_map):
        try:
            logging.error(f"entrou no create_employe_seduc employe seduc service")
            with employe_seduc.EmployeSeducDAO() as dao:
                logging.error(f"entrou no baseDAO employe seduc service")
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
            return False
        except Exception as e:
            return False

    def delete_employe_seduc(id):
        try:
            with employe_seduc.EmployeSeducDAO() as dao:
                dao.delete_employe_seduc(id)
            return True
        except Exception as e:
            return False

    def find_all(self):
        try:
            with employe_seduc.EmployeSeducDAO() as dao:
                result = dao.find_all()
            return result
        except Exception as e:
            return []

    def find_by_id(self, id):
        logging.error(f"entrou no find_by_id employe seduc service")
        try:
            with employe_seduc.EmployeSeducDAO() as dao:
                logging.error(f"entrou no baseDAO employe seduc service")
                return dao.find_by_id(id)
        except Exception as e:
            logging.error(f"Erro ao buscar empregado por id: {e}")
            return None

    def find_by_cpf(self, cpf):
        try:
            with employe_seduc.EmployeSeducDAO() as dao:
                return dao.find_by_cpf(cpf)
        except Exception as e:
            return None
        

    def find_all_orders_by_status(self, status):
        try:
            with order.OrderDAO() as dao:
                return dao.find_all_orders_by_status(status)
        except Exception as e:
            #logging.error(f"Erro ao buscar order por status: {e}")
            return None

    def find_all_orders_by_multiple_status(self, status):
        logging.error(f"entrou no find_all_orders_by_multiple_status employe seduc service")
        try:
            with order.OrderDAO() as dao:
                logging.error(f"entrou no with orders find_all_orders_by_multiple_status employe seduc service")
                return dao.find_all_orders_by_multiple_status(status)
        except Exception as e:
            logging.error(f"Erro ao buscar orders por status: {e}")
            return None