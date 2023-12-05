from flask import Blueprint, request, jsonify
from service.employe_seduc_services import EmployeSeducServices
import json
import logging

employe_seduc_services = EmployeSeducServices()

employe_seduc_blueprint = Blueprint('employe_seduc', __name__, url_prefix='/seduc')


"""
       CONTROLEERS employe Seduc
"""
@employe_seduc_blueprint.route('/find_all_employes', methods=['GET'])
def find_all_employe_seducs():
    try:
        logging.debug("Iniciando busca de todos os empregados da SEDUC.")
        employe_seducs = employe_seduc_services.find_all()
        if employe_seducs:
            # Converte cada modelo EmployeSeduc em um dicionário
            employe_seducs_maps = [employe_seduc.to_map() for employe_seduc in employe_seducs]
            # Converte a lista de dicionários em JSON
            return jsonify(employe_seducs_maps), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar empregados: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@employe_seduc_blueprint.route('/create_employe_seduc', methods=['POST'])    
def create_employe_seduc():

     # Passa o mapa para a camada de serviços
    try:
        employe_seduc_map = json.loads(request.data)
        success = EmployeSeducServices.create_employe_seduc(employe_seduc_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        #logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        #logging.error(f"Erro ao criar empregado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@employe_seduc_blueprint.route('/update_employe_seduc/<int:id>', methods=['PUT'])
def update_employe_seduc(id):
    try:
        employe_seduc_map = json.loads(request.data)
        success = EmployeSeducServices.update_employe_seduc(id, employe_seduc_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        #logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        #logging.error(f"Erro ao atualizar empregado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@employe_seduc_blueprint.route('/delete_employe_seduc/<int:id>', methods=['DELETE'])
def delete_employe_seduc(id):
    try:
        success = EmployeSeducServices.delete_employe_seduc(id)
        return jsonify({"status": "success" if success else "failed"}), 200
    except Exception as e:
        #logging.error(f"Erro ao deletar empregado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@employe_seduc_blueprint.route('/find_employe_by_cpf/<string:cpf>', methods=['GET'])
def find_employe_seduc_by_cpf(cpf):
    try:
        employe_seduc = employe_seduc_services.find_by_cpf(cpf)
        if employe_seduc:
            return employe_seduc.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar empregado por CPF: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@employe_seduc_blueprint.route('/find_employe_by_id/<int:id>', methods=['GET'])
def find_employe_seduc_by_id(id):
    try:
        employe_seduc = employe_seduc_services.find_by_id(id)
        if employe_seduc:
            return employe_seduc.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar empregado por ID: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    

##############################################################################################################

 ###### PREENCHIMENTO DA PÁGINAS DE PEDIDOS E HISTÓRICO DE PEDIDOS ######

##############################################################################################################

@employe_seduc_blueprint.route('/orders', methods=['GET'])
def find_orders_activate():
    logging.debug("Iniciando busca de todos os orders ativos.")
    try:
        orders = employe_seduc_services.find_all_orders_by_multiple_status(["Criado", "Confirmado", "Despachado"])
        logging.debug("Passou try controller.")
        logging.debug(orders)
        if orders:
            # Converte cada modelo Order em um dicionário
            logging.debug("Passou if orders, controllers.")
            orders_maps = [order.to_map() for order in orders]
            # Converte a lista de dicionários em JSON
            return jsonify(orders_maps), 200
        else:
            logging.debug("Passou else orders, controllers.")
            logging.error("Erro ao buscar orders ativos: {e}")
            return {"status": "not found"}, 404
    except Exception as e:
        logging.error(f"Erro ao buscar orders ativos: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@employe_seduc_blueprint.route('/history', methods=['GET'])
def find_orders_delivered():
    logging.debug("Iniciando busca de todos os orders inativos.")
    try:
        orders = employe_seduc_services.find_all_orders_by_multiple_status(["Entregue", "Avaliado"])
        logging.debug("Passou try controller.")
        if orders:
            # Converte cada modelo Order em um dicionário
            logging.debug("Passou if orders, controllers.")
            orders_maps = [order.to_map() for order in orders]
            # Converte a lista de dicionários em JSON
            return jsonify(orders_maps), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar orders ativos: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
                               

