import logging
from models import transporter

class TransporterServices:

    def create_transporter(transporter_map):
        try:
            with transporter.TransporterDAO() as dao:
                dao.create_transporter(transporter_map)
            return True
        except (ValueError, TypeError) as e:
            return False
        except Exception as e:
            return False
        
    def create_transporters(transporters_data):
        try:
            with transporter.TransporterDAO() as dao:
                dao.create_transporters(transporters_data)
            return True
        except (ValueError, TypeError) as e:
            return False
        except Exception as e:
            return False

    def update_transporter(id, transporter_map):
        try:
            with transporter.TransporterDAO() as dao:
                dao.update_transporter(id, transporter_map)
            return True
        except (ValueError, TypeError) as e:
            return False
        except Exception as e:
            return False

    def delete_transporter(id):
        try:
            with transporter.TransporterDAO() as dao:
                dao.delete_transporter(id)
            return True
        except Exception as e:
            return False
        
    def delete_all_transporters():
        try:
            with transporter.TransporterDAO() as dao:
                dao.delete_all_transporters()
            return True
        except Exception as e:
            return False

    def find_all(self):
        try:
            with transporter.TransporterDAO() as dao:
                result = dao.find_all()
            return result
        except Exception as e:
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
            return None
        