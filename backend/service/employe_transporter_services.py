import logging
from models import order
from models import employe_transporter


class EmployeTransporterServices:

    def create_employe_transporter(employe_transporter_map):
        try:
            with employe_transporter.EmployeTransporterDAO() as dao:
                dao.create_employe_transporter(employe_transporter_map)
            return True
        except (ValueError, TypeError) as e:
            #logging.error(f"Erro de dados ao criar empregado: {e}")
            return False
        except Exception as e:
            #logging.error(f"Erro inesperado ao criar empregado: {e}")
            return False

    def update_employe_transporter(id, employe_transporter_map):
        try:
            with employe_transporter.EmployeTransporterDAO() as dao:
                dao.update_employe_transporter(id, employe_transporter_map)
            return True
        except (ValueError, TypeError) as e:
            #logging.error(f"Erro de dados ao atualizar empregado: {e}")
            return False
        except Exception as e:
            #logging.error(f"Erro inesperado ao atualizar empregado: {e}")
            return False

    def delete_employe_transporter(id):
        try:
            with employe_transporter.EmployeTransporterDAO() as dao:
                dao.delete_employe_transporter(id)
            return True
        except Exception as e:
            #logging.error(f"Erro ao deletar empregado: {e}")
            return False

    def find_all(self):
        try:
            with employe_transporter.EmployeTransporterDAO() as dao:
                result = dao.find_all()
            return result
        except Exception as e:
            #logging.error(f"Erro ao buscar todos os empregados: {e}")
            return []

    def find_by_id(self, id):
        try:
            with employe_transporter.EmployeTransporterDAO() as dao:
                return dao.find_by_id(id)
        except Exception as e:
            #logging.error(f"Erro ao buscar empregado por id: {e}")
            return None

    def find_by_cpf(self, cpf):
        try:
            with employe_transporter.EmployeTransporterDAO() as dao:
                return dao.find_by_cpf(cpf)
        except Exception as e:
            #logging.error(f"Erro ao buscar empregado por cpf: {e}")
            return None
        

##############################################################################################################

 ###### PREENCHIMENTO DA PÁGINAS DE PEDIDOS E HISTÓRICO DE PEDIDOS ######

##############################################################################################################


    def find_all_orders_by_multiple_status_and_transporter_id(self, status, transporter_id):
        logging.error(f"entrou no find_all_orders_by_multiple_status employe transporter service")
        try:
            with order.OrderDAO() as dao:
                logging.error(f"entrou no with orders find_all_orders_by_multiple_status employe seduc service")
                return dao.find_all_orders_by_multiple_status_and_transporter_id(status, transporter_id)
        except Exception as e:
            logging.error(f"Erro ao buscar orders por status: {e}")
            return None
        