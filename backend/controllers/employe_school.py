from flask import Blueprint, request, jsonify
from service.school_services import SchoolServices
from service.employe_school_services import EmployeSchoolServices
import json
import logging

employe_school_services = EmployeSchoolServices()
school_services = SchoolServices()

employe_school_blueprint = Blueprint('employe_school', __name__, url_prefix='/school')


"""
       CONTROLEERS employe School
"""
@employe_school_blueprint.route('/find_all_employes', methods=['GET'])
def find_all_employe_schools():
    try:
        logging.debug("Iniciando busca de todos os empregados da School.")
        employe_schools = employe_school_services.find_all()
        if employe_schools:
            # Converte cada modelo EmployeSchool em um dicionário
            employe_schools_maps = [employe_school.to_map() for employe_school in employe_schools]
            # Converte a lista de dicionários em JSON
            return jsonify(employe_schools_maps), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        logging.error(f"Erro ao buscar empregados: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@employe_school_blueprint.route('/create_employe_school', methods=['POST'])    
def create_employe_school():
    try:
        employe_school_map = json.loads(request.data)
        success = EmployeSchoolServices.create_employe_school(employe_school_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        logging.error(f"Erro ao criar empregado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@employe_school_blueprint.route('/update_employe_school/<int:id>', methods=['PUT'])
def update_employe_school(id):
    try:
        employe_school_map = json.loads(request.data)
        success = EmployeSchoolServices.update_employe_school(id, employe_school_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        logging.error(f"Erro ao atualizar empregado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@employe_school_blueprint.route('/delete_employe_school/<int:id>', methods=['DELETE'])
def delete_employe_school(id):
    try:
        success = EmployeSchoolServices.delete_employe_school(id)
        return jsonify({"status": "success" if success else "failed"}), 200
    except Exception as e:
        logging.error(f"Erro ao deletar empregado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@employe_school_blueprint.route('/find_employe_by_cpf/<string:cpf>', methods=['GET'])
def find_employe_school_by_cpf(cpf):
    try:
        employe_school = employe_school_services.find_by_cpf(cpf)
        if employe_school:
            return employe_school.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        logging.error(f"Erro ao buscar empregado por CPF: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@employe_school_blueprint.route('/find_employe_by_id/<int:id>', methods=['GET'])
def find_employe_school_by_id(id):
    try:
        employe_school = employe_school_services.find_by_id(id)
        if employe_school:
            return employe_school.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        logging.error(f"Erro ao buscar empregado por ID: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

