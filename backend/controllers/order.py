from flask import Blueprint, request, jsonify
from service.order_services import OrderServices
import json
import logging
from cache_config import cache
order_services = OrderServices()

order_blueprint = Blueprint('order', __name__, url_prefix='/order')


@order_blueprint.route('/create_order', methods=['POST'])
def create_order():
    try:
        order_map = json.loads(request.data)
        success = OrderServices.create_order(order_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        logging.error(f"Erro ao criar empregado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    

@order_blueprint.route('/create_orders', methods=['POST'])
def create_orders():
    try:
        orders_data = json.loads(request.data) # Espera-se uma lista de dicionários
        success = OrderServices.create_orders(orders_data)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        logging.error(f"Erro ao criar fornecedores: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@order_blueprint.route('/update_order/<int:id>', methods=['PUT'])
def update_order(id):
    try:
        order_map = json.loads(request.data)
        success = OrderServices.update_order(id, order_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        logging.error(f"Erro ao atualizar fornecedor: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@order_blueprint.route('/delete_order/<int:id>', methods=['DELETE'])
def delete_order(id):
    try:
        success = OrderServices.delete_order(id)
        return jsonify({"status": "success" if success else "failed"}), 200
    except Exception as e:
        logging.error(f"Erro ao deletar fornecedor: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@order_blueprint.route('/find_order_by_cnpj/<string:cnpj>', methods=['GET'])
def find_order_by_cnpj(cnpj):
    try:
        order = order_services.find_by_cnpj(cnpj)
        if order:
            return order.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        logging.error(f"Erro ao buscar fornecedor por CNPJ: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@order_blueprint.route('/find_order_by_id/<int:id>', methods=['GET'])
def find_order_by_id(id):
    try:
        order = order_services.find_by_id(id)
        if order:
            logging.error(f"chegou jsonfy")
            return order.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        logging.error(f"Erro ao buscar fornecedor por ID: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    


# @order_blueprint.route('/find_all_orders', methods=['GET'])
# def find_all_orders():
#     try:
#         logging.debug("Iniciando busca de todas fornecedors.")
#         orders = order_services.find_all()
#         if orders:
#             # Converte cada modelo Order em um dicionário
#             orders_maps = [order.to_map() for order in orders]
#             # Converte a lista de dicionários em JSON
#             return jsonify(orders_maps), 200
            
#         else:
#             return {"status": "not found"}, 404
#     except Exception as e:
#         #logging.error(f"Erro ao buscar fornecedors: {e}")
#         return jsonify({"status": "error", "message": str(e)}), 500

@order_blueprint.route('/find_all_orders', methods=['GET'])
@cache.cached(timeout=50000)
def find_all_orders():
    try:
        logging.debug("Iniciando busca de todas fornecedors.")
        orders = order_services.find_all()
        if orders:
            orders_maps = [order.to_map() for order in orders]
            return jsonify(orders_maps), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
