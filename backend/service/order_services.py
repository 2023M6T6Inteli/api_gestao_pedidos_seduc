import logging
from models import order


class OrderServices:

    def create_order(order_map):
        try:
            with order.OrderDAO() as dao:
                dao.create_order(order_map)   
            return True
        except (ValueError, TypeError) as e:
            logging.error(f"Erro de dados ao criar order: {e}")
            return False
        except Exception as e:
            logging.error(f"Erro inesperado OrderService ao criar order: {e}")
            return False
        
    def create_orders(orders_data):
        try:
            with order.OrderDAO() as dao:
                dao.create_orders(orders_data)
            return True
        except (ValueError, TypeError) as e:
            return False
        except Exception as e:
            return False

    def update_order(id, order_map):
        try:
            with order.OrderDAO() as dao:
                dao.update_order(id, order_map)
            return True
        except (ValueError, TypeError) as e:
            return False
        except Exception as e:
            return False

    def delete_order(id):
        try:
            with order.OrderDAO() as dao:
                dao.delete_order(id)
            return True
        except Exception as e:
            return False
        
    def delete_all_orders():
        try:
            with order.OrderDAO() as dao:
                dao.delete_all_orders()
            return True
        except Exception as e:
            return False

    def find_all(self):
        logging.error(f"chegou service")
        try:
            with order.OrderDAO() as dao:
                logging.error(f"chegou service dao")
                result = dao.find_all()
            return result
        except Exception as e:
            logging.error(f"Erro ao buscar todos os orders: {e}")
            return []

    def find_by_id(self, id):
        try:
            with order.OrderDAO() as dao:
                return dao.find_by_id(id)
        except Exception as e:
            logging.error(f"Erro ao buscar order por id: {e}")
            return None
        

    def get_details_by_id(self, id):
        try:
            with order.OrderDAO() as dao:
                return dao.get_details_by_id(id)
        except Exception as e:
            return None
        
