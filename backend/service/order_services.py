import logging
from models import order


class OrderServices:

    def create_order(order_map):
        try:
            with order.OrderDAO() as dao:
                logging.error(f"dados recebidos: {order_map}")
                dao.create_order(order_map)
                logging.error(f"dadoS recebidos: {order_map}")
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
            logging.error(f"Erro de dados ao criar order: {e}")
            return False
        except Exception as e:
            logging.error(f"Erro inesperado ao criar orders: {e}")
            return False

    def update_order(id, order_map):
        try:
            with order.OrderDAO() as dao:
                dao.update_order(id, order_map)
            return True
        except (ValueError, TypeError) as e:
            logging.error(f"Erro de dados ao atualizar order: {e}")
            return False
        except Exception as e:
            logging.error(f"Erro inesperado ao atualizar order: {e}")
            return False

    def delete_order(id):
        try:
            with order.OrderDAO() as dao:
                dao.delete_order(id)
            return True
        except Exception as e:
            logging.error(f"Erro ao deletar order: {e}")
            return False
        
    def delete_all_orders():
        try:
            with order.OrderDAO() as dao:
                dao.delete_all_orders()
            return True
        except Exception as e:
            logging.error(f"Erro ao deletar todas as escolas: {e}")
            return False

    def find_all(self):
        try:
            with order.OrderDAO() as dao:
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

    # def find_by_cnpj(self, cnpj):
    #     try:
    #         with order.OrderDAO() as dao:
    #             return dao.find_by_cnpj(cnpj)
    #     except Exception as e:
    #         logging.error(f"Erro ao buscar order por cnpj: {e}")
    #         return None
        