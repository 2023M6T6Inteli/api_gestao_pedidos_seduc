from flask import Blueprint, request, jsonify
from service.school_services import SchoolServices
import json
import logging

school_services = SchoolServices()

school_blueprint = Blueprint('school', __name__, url_prefix='/school')


@school_blueprint.route('/create_school', methods=['POST'])
def create_school():
    try:
        school_map = json.loads(request.data)
        success = SchoolServices.create_school(school_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        #logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        #logging.error(f"Erro ao criar empregado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    

@school_blueprint.route('/create_schools', methods=['POST'])
def create_schools():
    try:
        schools_data = json.loads(request.data) # Espera-se uma lista de dicionários
        success = SchoolServices.create_schools(schools_data)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        #logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        #logging.error(f"Erro ao criar escolas: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@school_blueprint.route('/update_school/<int:id>', methods=['PUT'])
def update_school(id):
    try:
        school_map = json.loads(request.data)
        success = SchoolServices.update_school(id, school_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        #logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        #logging.error(f"Erro ao atualizar escola: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@school_blueprint.route('/delete_school/<int:id>', methods=['DELETE'])
def delete_school(id):
    try:
        success = SchoolServices.delete_school(id)
        return jsonify({"status": "success" if success else "failed"}), 200
    except Exception as e:
        #logging.error(f"Erro ao deletar escola: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@school_blueprint.route('/find_school_by_cnpj/<string:cnpj>', methods=['GET'])
def find_school_by_cnpj(cnpj):
    try:
        school = school_services.find_by_cnpj(cnpj)
        if school:
            return school.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar escola por CNPJ: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@school_blueprint.route('/find_school_by_id/<int:id>', methods=['GET'])
def find_school_by_id(id):
    try:
        school = school_services.find_by_id(id)
        if school:
            return school.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar escola por ID: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    

@school_blueprint.route('/find_all_schools', methods=['GET'])
def find_all_schools():
    try:
        logging.debug("Iniciando busca de todas escolas.")
        schools = school_services.find_all()
        if schools:
            # Converte cada modelo School em um dicionário
            schools_maps = [school.to_map() for school in schools]
            # Converte a lista de dicionários em JSON
            return jsonify(schools_maps), 200
            
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar escolas: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
