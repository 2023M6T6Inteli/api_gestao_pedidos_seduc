import logging
from models import transporter


class TransporterServices:

    def create_transporter(transporter_map):
        try:
            with transporter.TransporterDAO() as dao:
                logging.error(f"dados recebidos: {transporter_map}")
                dao.create_transporter(transporter_map)
                logging.error(f"dadoa recebidos: {transporter_map}")
            return True
        except (ValueError, TypeError) as e:
            logging.error(f"Erro de dados ao criar transporter: {e}")
            return False
        except Exception as e:
            logging.error(f"Erro inesperado TransporterService ao criar transporter: {e}")
            return False
        
    def create_transporters(transporters_data):
        try:
            with transporter.TransporterDAO() as dao:
                dao.create_transporters(transporters_data)
            return True
        except (ValueError, TypeError) as e:
            logging.error(f"Erro de dados ao criar transporter: {e}")
            return False
        except Exception as e:
            logging.error(f"Erro inesperado ao criar transporters: {e}")
            return False

    def update_transporter(id, transporter_map):
        try:
            with transporter.TransporterDAO() as dao:
                dao.update_transporter(id, transporter_map)
            return True
        except (ValueError, TypeError) as e:
            logging.error(f"Erro de dados ao atualizar transporter: {e}")
            return False
        except Exception as e:
            logging.error(f"Erro inesperado ao atualizar transporter: {e}")
            return False

    def delete_transporter(id):
        try:
            with transporter.TransporterDAO() as dao:
                dao.delete_transporter(id)
            return True
        except Exception as e:
            logging.error(f"Erro ao deletar transporter: {e}")
            return False
        
    def delete_all_transporters():
        try:
            with transporter.TransporterDAO() as dao:
                dao.delete_all_transporters()
            return True
        except Exception as e:
            logging.error(f"Erro ao deletar todas as escolas: {e}")
            return False

    def find_all(self):
        try:
            with transporter.TransporterDAO() as dao:
                result = dao.find_all()
            return result
        except Exception as e:
            logging.error(f"Erro ao buscar todos os transporters: {e}")
            return []

    def find_by_id(self, id):
        try:
            with transporter.TransporterDAO() as dao:
                return dao.find_by_id(id)
        except Exception as e:
            logging.error(f"Erro ao buscar transporter por id: {e}")
            return None

    def find_by_cnpj(self, cnpj):
        try:
            with transporter.TransporterDAO() as dao:
                return dao.find_by_cnpj(cnpj)
        except Exception as e:
            logging.error(f"Erro ao buscar transporter por cnpj: {e}")
            return None
        