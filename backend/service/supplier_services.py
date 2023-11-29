import logging
from models import supplier


class SupplierServices:

    def create_supplier(supplier_map):
        try:
            with supplier.SupplierDAO() as dao:
                #logging.error(f"dados recebidos: {supplier_map}")
                dao.create_supplier(supplier_map)
                #logging.error(f"dadoa recebidos: {supplier_map}")
            return True
        except (ValueError, TypeError) as e:
            #logging.error(f"Erro de dados ao criar supplier: {e}")
            return False
        except Exception as e:
            #logging.error(f"Erro inesperado SupplierService ao criar supplier: {e}")
            return False
        
    def create_suppliers(suppliers_data):
        try:
            with supplier.SupplierDAO() as dao:
                dao.create_suppliers(suppliers_data)
            return True
        except (ValueError, TypeError) as e:
            #logging.error(f"Erro de dados ao criar supplier: {e}")
            return False
        except Exception as e:
            #logging.error(f"Erro inesperado ao criar suppliers: {e}")
            return False

    def update_supplier(id, supplier_map):
        try:
            with supplier.SupplierDAO() as dao:
                dao.update_supplier(id, supplier_map)
            return True
        except (ValueError, TypeError) as e:
            #logging.error(f"Erro de dados ao atualizar supplier: {e}")
            return False
        except Exception as e:
            #logging.error(f"Erro inesperado ao atualizar supplier: {e}")
            return False

    def delete_supplier(id):
        try:
            with supplier.SupplierDAO() as dao:
                dao.delete_supplier(id)
            return True
        except Exception as e:
            #logging.error(f"Erro ao deletar supplier: {e}")
            return False
        
    def delete_all_suppliers():
        try:
            with supplier.SupplierDAO() as dao:
                dao.delete_all_suppliers()
            return True
        except Exception as e:
            #logging.error(f"Erro ao deletar todas as escolas: {e}")
            return False

    def find_all(self):
        try:
            with supplier.SupplierDAO() as dao:
                result = dao.find_all()
            return result
        except Exception as e:
            #logging.error(f"Erro ao buscar todos os suppliers: {e}")
            return []

    def find_by_id(self, id):
        try:
            with supplier.SupplierDAO() as dao:
                return dao.find_by_id(id)
        except Exception as e:
            #logging.error(f"Erro ao buscar supplier por id: {e}")
            return None

    def find_by_cnpj(self, cnpj):
        try:
            with supplier.SupplierDAO() as dao:
                return dao.find_by_cnpj(cnpj)
        except Exception as e:
            #logging.error(f"Erro ao buscar supplier por cnpj: {e}")
            return None
        