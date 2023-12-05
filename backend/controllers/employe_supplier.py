from flask import Blueprint, request, jsonify
from service.employe_supplier_services import EmployeSupplierServices
import json
import logging

employe_supplier_services = EmployeSupplierServices()

employe_supplier_blueprint = Blueprint('employe_supplier', __name__, url_prefix='/supplier')


"""
       CONTROLEERS employe Supplier
"""
@employe_supplier_blueprint.route('/find_all_employes', methods=['GET'])
def find_all_employe_suppliers():
    try:
        logging.debug("Iniciando busca de todos os empregados da fornecedora.")
        employe_suppliers = employe_supplier_services.find_all()
        if employe_suppliers:
            # Converte cada modelo EmployeSupplier em um dicionário
            employe_suppliers_maps = [employe_supplier.to_map() for employe_supplier in employe_suppliers]
            # Converte a lista de dicionários em JSON
            return jsonify(employe_suppliers_maps), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar empregados: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@employe_supplier_blueprint.route('/create_employe_supplier', methods=['POST'])    
def create_employe_supplier():
    try:
        employe_supplier_map = json.loads(request.data)
        success = EmployeSupplierServices.create_employe_supplier(employe_supplier_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        #logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        #logging.error(f"Erro ao criar empregado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@employe_supplier_blueprint.route('/update_employe_supplier/<int:id>', methods=['PUT'])
def update_employe_supplier(id):
    try:
        employe_supplier_map = json.loads(request.data)
        success = EmployeSupplierServices.update_employe_supplier(id, employe_supplier_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        #logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        #logging.error(f"Erro ao atualizar empregado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@employe_supplier_blueprint.route('/delete_employe_supplier/<int:id>', methods=['DELETE'])
def delete_employe_supplier(id):
    try:
        success = EmployeSupplierServices.delete_employe_supplier(id)
        return jsonify({"status": "success" if success else "failed"}), 200
    except Exception as e:
        #logging.error(f"Erro ao deletar empregado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@employe_supplier_blueprint.route('/find_employe_by_cpf/<string:cpf>', methods=['GET'])
def find_employe_supplier_by_cpf(cpf):
    try:
        employe_supplier = employe_supplier_services.find_by_cpf(cpf)
        if employe_supplier:
            return employe_supplier.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar empregado por CPF: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@employe_supplier_blueprint.route('/find_employe_by_id/<int:id>', methods=['GET'])
def find_employe_supplier_by_id(id):
    try:
        employe_supplier = employe_supplier_services.find_by_id(id)
        if employe_supplier:
            return employe_supplier.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar empregado por ID: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    


##############################################################################################################

 ###### PREENCHIMENTO DA PÁGINAS DE PEDIDOS E HISTÓRICO DE PEDIDOS ######

##############################################################################################################


@employe_supplier_blueprint.route('/orders/<int:supplier_id>', methods=['GET'])
def find_orders_activate(supplier_id):
    logging.debug("Iniciando busca de todos os orders ativos.")
    try:
        orders = employe_supplier_services.find_all_orders_by_multiple_status_and_supplier_id(["Criado", "Confirmado", "Despachado"], supplier_id)
        if orders:
            # Converte cada modelo Order em um dicionário
            orders_maps = [order.to_map() for order in orders]
            # Converte a lista de dicionários em JSON
            return jsonify(orders_maps), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar orders ativos: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    

@employe_supplier_blueprint.route('/history/<int:supplier_id>', methods=['GET'])
def find_orders_delivered(supplier_id):
    logging.debug("Iniciando busca de todos os orders ativos.")
    try:
        orders = employe_supplier_services.find_all_orders_by_multiple_status_and_supplier_id(["Entregue", "Avaliado"], supplier_id)
        if orders:
            # Converte cada modelo Order em um dicionário
            orders_maps = [order.to_map() for order in orders]
            # Converte a lista de dicionários em JSON
            return jsonify(orders_maps), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar orders ativos: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500