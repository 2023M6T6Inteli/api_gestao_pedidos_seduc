# Flask App

import logging
from flask import Flask, request, jsonify
from cache_config import cache
# from service.academic_services import AcademicServices
from controllers.employe_seduc import employe_seduc_blueprint
from controllers.employe_supplier import employe_supplier_blueprint
from controllers.employe_transporter import employe_transporter_blueprint
from controllers.employe_school import employe_school_blueprint
from controllers.supplier import supplier_blueprint
from controllers.school import school_blueprint
from controllers.transporter import transporter_blueprint
from controllers.order import order_blueprint
from controllers.login import login_blueprint
from flask_jwt_extended import (
    JWTManager
)
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'


cache.init_app(app)
jwt = JWTManager(app)


app.register_blueprint(employe_seduc_blueprint)
app.register_blueprint(employe_supplier_blueprint)
app.register_blueprint(employe_transporter_blueprint)
app.register_blueprint(employe_school_blueprint)
app.register_blueprint(supplier_blueprint)
app.register_blueprint(school_blueprint)
app.register_blueprint(transporter_blueprint)
app.register_blueprint(order_blueprint)
app.register_blueprint(login_blueprint)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    
if __name__ == '__main__':
    app.run(debug=True)
    

