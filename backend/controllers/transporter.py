from flask import Blueprint, request, jsonify
from service.transporter_services import TransporterServices
import json
import logging

transporter_services = TransporterServices()

transporter_blueprint = Blueprint('transporter', __name__, url_prefix='/transporter')


@transporter_blueprint.route('/create_transporter', methods=['POST'])
def create_transporter():
    try:
        transporter_map = json.loads(request.data)
        success = TransporterServices.create_transporter(transporter_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        #logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        #logging.error(f"Erro ao criar transportadora: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    

@transporter_blueprint.route('/create_transporters', methods=['POST'])
def create_transporters():
    try:
        transporters_data = json.loads(request.data) # Espera-se uma lista de dicionários
        success = TransporterServices.create_transporters(transporters_data)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        #logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        #logging.error(f"Erro ao criar transportadoras: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@transporter_blueprint.route('/update_transporter/<int:id>', methods=['PUT'])
def update_transporter(id):
    try:
        transporter_map = json.loads(request.data)
        success = TransporterServices.update_transporter(id, transporter_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        #logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        #logging.error(f"Erro ao atualizar transportadora: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@transporter_blueprint.route('/delete_transporter/<int:id>', methods=['DELETE'])
def delete_transporter(id):
    try:
        success = TransporterServices.delete_transporter(id)
        return jsonify({"status": "success" if success else "failed"}), 200
    except Exception as e:
        #logging.error(f"Erro ao deletar transportadora: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@transporter_blueprint.route('/find_transporter_by_cnpj/<string:cnpj>', methods=['GET'])
def find_transporter_by_cnpj(cnpj):
    try:
        transporter = transporter_services.find_by_cnpj(cnpj)
        if transporter:
            return transporter.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar transportadora por CNPJ: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@transporter_blueprint.route('/find_transporter_by_id/<int:id>', methods=['GET'])
def find_transporter_by_id(id):
    try:
        transporter = transporter_services.find_by_id(id)
        if transporter:
            return transporter.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar transportadora por ID: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    

@transporter_blueprint.route('/find_all_transporters', methods=['GET'])
def find_all_transporters():
    try:
        logging.debug("Iniciando busca de todas transportadoras.")
        transporters = transporter_services.find_all()
        if transporters:
            # Converte cada modelo School em um dicionário
            transporters_maps = [transporter.to_map() for transporter in transporters]
            # Converte a lista de dicionários em JSON
            return jsonify(transporters_maps), 200
            
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar transportadoras: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
