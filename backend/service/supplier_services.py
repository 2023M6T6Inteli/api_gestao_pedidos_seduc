import logging
from models import supplier


class SupplierServices:

    def create_supplier(supplier_map):
        try:
            with supplier.SupplierDAO() as dao:
                dao.create_supplier(supplier_map)
            return True
        except (ValueError, TypeError) as e:
            return False
        except Exception as e:
            return False
        
    def create_suppliers(suppliers_data):
        try:
            with supplier.SupplierDAO() as dao:
                dao.create_suppliers(suppliers_data)
            return True
        except (ValueError, TypeError) as e:
            return False
        except Exception as e:
            return False

    def update_supplier(id, supplier_map):
        try:
            with supplier.SupplierDAO() as dao:
                dao.update_supplier(id, supplier_map)
            return True
        except (ValueError, TypeError) as e:
            return False
        except Exception as e:
            return False

    def delete_supplier(id):
        try:
            with supplier.SupplierDAO() as dao:
                dao.delete_supplier(id)
            return True
        except Exception as e:
            return False
        
    def delete_all_suppliers():
        try:
            with supplier.SupplierDAO() as dao:
                dao.delete_all_suppliers()
            return True
        except Exception as e:
            return False

    def find_all(self):
        try:
            with supplier.SupplierDAO() as dao:
                result = dao.find_all()
            return result
        except Exception as e:
            return []

    def find_by_id(self, id):
        try:
            with supplier.SupplierDAO() as dao:
                return dao.find_by_id(id)
        except Exception as e:
            return None

    def find_by_cnpj(self, cnpj):
        try:
            with supplier.SupplierDAO() as dao:
                return dao.find_by_cnpj(cnpj)
        except Exception as e:
            return None
        