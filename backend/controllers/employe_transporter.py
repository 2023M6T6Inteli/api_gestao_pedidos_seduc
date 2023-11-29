from flask import Blueprint, request, jsonify
from service.employe_transporter_services import EmployeTransporterServices
import json
import logging

employe_transporter_services = EmployeTransporterServices()

employe_transporter_blueprint = Blueprint('employe_transporter', __name__, url_prefix='/transporter')


"""
       CONTROLEERS employe Transporter
"""
@employe_transporter_blueprint.route('/find_all_employes', methods=['GET'])
def find_all_employe_transporters():
    try:
        logging.debug("Iniciando busca de todos os empregados da Transporter.")
        employe_transporters = employe_transporter_services.find_all()
        if employe_transporters:
            # Converte cada modelo EmployeTransporter em um dicionário
            employe_transporters_maps = [employe_transporter.to_map() for employe_transporter in employe_transporters]
            # Converte a lista de dicionários em JSON
            return jsonify(employe_transporters_maps), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar empregados: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@employe_transporter_blueprint.route('/create_employe_transporter', methods=['POST'])    
def create_employe_transporter():
    try:
        employe_transporter_map = json.loads(request.data)
        success = EmployeTransporterServices.create_employe_transporter(employe_transporter_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        #logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        #logging.error(f"Erro ao criar empregado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@employe_transporter_blueprint.route('/update_employe_transporter/<int:id>', methods=['PUT'])
def update_employe_transporter(id):
    try:
        employe_transporter_map = json.loads(request.data)
        success = EmployeTransporterServices.update_employe_transporter(id, employe_transporter_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        #logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        #logging.error(f"Erro ao atualizar empregado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@employe_transporter_blueprint.route('/delete_employe_transporter/<int:id>', methods=['DELETE'])
def delete_employe_transporter(id):
    try:
        success = EmployeTransporterServices.delete_employe_transporter(id)
        return jsonify({"status": "success" if success else "failed"}), 200
    except Exception as e:
        #logging.error(f"Erro ao deletar empregado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@employe_transporter_blueprint.route('/find_employe_by_cpf/<string:cpf>', methods=['GET'])
def find_employe_transporter_by_cpf(cpf):
    try:
        employe_transporter = employe_transporter_services.find_by_cpf(cpf)
        if employe_transporter:
            return employe_transporter.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar empregado por CPF: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@employe_transporter_blueprint.route('/find_employe_by_id/<int:id>', methods=['GET'])
def find_employe_transporter_by_id(id):
    try:
        employe_transporter = employe_transporter_services.find_by_id(id)
        if employe_transporter:
            return employe_transporter.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar empregado por ID: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    

##############################################################################################################

 ###### PREENCHIMENTO DA PÁGINAS DE PEDIDOS E HISTÓRICO DE PEDIDOS ######

##############################################################################################################


@employe_transporter_blueprint.route('/orders/<int:transporter_id>', methods=['GET'])
def find_orders_activate(transporter_id):
    logging.debug("Iniciando busca de todos os orders ativos.")
    try:
        orders = employe_transporter_services.find_all_orders_by_multiple_status_and_transporter_id(["Criado", "Confirmado", "Em Trânsito"], transporter_id)
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
    

@employe_transporter_blueprint.route('/history/<int:transporter_id>', methods=['GET'])
def find_orders_delivered(transporter_id):
    logging.debug("Iniciando busca de todos os orders ativos.")
    try:
        orders = employe_transporter_services.find_all_orders_by_multiple_status_and_transporter_id(["Entregue", "Cancelado"], transporter_id)
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

