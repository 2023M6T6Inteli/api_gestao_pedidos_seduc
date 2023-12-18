from flask import Blueprint, request, jsonify
from service.login_services import LoginServices
from service.order_services import OrderServices
import json
import logging
from cache_config import cache
from flask_jwt_extended import (create_access_token)

login_services = LoginServices()

order_blueprint = Blueprint('order', __name__, url_prefix='/auth')


@order_blueprint.route('/login', methods=['POST'])
def login():
    try:
        login_map = json.loads(request.data)

        # Verifique se os campos 'email' e 'password' estão presentes no JSON
        if 'email' not in login_map or 'password' not in login_map:
            return jsonify({'message': 'Dados de autenticação incompletos'}), 400

        sucess = login_services.login(login_map)

        if sucess:
            # Autenticação bem-sucedida, crie um token JWT
            access_token = create_access_token(identity=sucess)

            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Credenciais inválidas'}), 401
    except Exception as e:
        return jsonify({'message': 'Erro inesperado'}), 500