from flask import Blueprint, request, jsonify
from service.supplier_services import SupplierServices
import json
import logging

supplier_services = SupplierServices()

supplier_blueprint = Blueprint('supplier', __name__, url_prefix='/supplier')


@supplier_blueprint.route('/create_supplier', methods=['POST'])
def create_supplier():
    try:
        supplier_map = json.loads(request.data)
        success = SupplierServices.create_supplier(supplier_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        #logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        #logging.error(f"Erro ao criar empregado: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    

@supplier_blueprint.route('/create_suppliers', methods=['POST'])
def create_suppliers():
    try:
        suppliers_data = json.loads(request.data) # Espera-se uma lista de dicionários
        success = SupplierServices.create_suppliers(suppliers_data)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        #logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        #logging.error(f"Erro ao criar fornecedores: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@supplier_blueprint.route('/update_supplier/<int:id>', methods=['PUT'])
def update_supplier(id):
    try:
        supplier_map = json.loads(request.data)
        success = SupplierServices.update_supplier(id, supplier_map)
        return jsonify({"status": "success" if success else "failed"}), 200
    except json.JSONDecodeError:
        #logging.error("JSON inválido recebido.")
        return jsonify({"status": "error", "message": "JSON inválido"}), 400
    except Exception as e:
        #logging.error(f"Erro ao atualizar fornecedor: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@supplier_blueprint.route('/delete_supplier/<int:id>', methods=['DELETE'])
def delete_supplier(id):
    try:
        success = SupplierServices.delete_supplier(id)
        return jsonify({"status": "success" if success else "failed"}), 200
    except Exception as e:
        #logging.error(f"Erro ao deletar fornecedor: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@supplier_blueprint.route('/find_supplier_by_cnpj/<string:cnpj>', methods=['GET'])
def find_supplier_by_cnpj(cnpj):
    try:
        supplier = supplier_services.find_by_cnpj(cnpj)
        if supplier:
            return supplier.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar fornecedor por CNPJ: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@supplier_blueprint.route('/find_supplier_by_id/<int:id>', methods=['GET'])
def find_supplier_by_id(id):
    try:
        supplier = supplier_services.find_by_id(id)
        if supplier:
            return supplier.jsonify(), 200
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar fornecedor por ID: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    

@supplier_blueprint.route('/find_all_suppliers', methods=['GET'])
def find_all_suppliers():
    try:
        logging.debug("Iniciando busca de todas fornecedors.")
        suppliers = supplier_services.find_all()
        if suppliers:
            # Converte cada modelo Supplier em um dicionário
            suppliers_maps = [supplier.to_map() for supplier in suppliers]
            # Converte a lista de dicionários em JSON
            return jsonify(suppliers_maps), 200
            
        else:
            return {"status": "not found"}, 404
    except Exception as e:
        #logging.error(f"Erro ao buscar fornecedors: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
