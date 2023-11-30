# Flask App

import logging
from flask import Flask, request, jsonify
# from service.academic_services import AcademicServices
from controllers.employe_seduc import employe_seduc_blueprint
from controllers.employe_supplier import employe_supplier_blueprint
from controllers.employe_transporter import employe_transporter_blueprint
from controllers.employe_school import employe_school_blueprint
from controllers.supplier import supplier_blueprint
from controllers.school import school_blueprint
from controllers.transporter import transporter_blueprint
from controllers.order import order_blueprint


app = Flask(__name__)
# academic_services = AcademicServices()

# Chamando meus contrllers para aplicação principal
app.register_blueprint(employe_seduc_blueprint)
app.register_blueprint(employe_supplier_blueprint)
app.register_blueprint(employe_transporter_blueprint)
app.register_blueprint(employe_school_blueprint)
app.register_blueprint(supplier_blueprint)
app.register_blueprint(school_blueprint)
app.register_blueprint(transporter_blueprint)
app.register_blueprint(order_blueprint)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# @app.route('/enroll_student', methods=['POST'])
# def enroll_student():
#     student_map = json.loads(request.data)
#     #print(student_map)
#     """
#     {
#         "ra": "RA001",
#         "nome": "Jeff"
#     }
#     """
#     # Passa o mapa para a camada de serviços
#     success = academic_services.enroll_student(student_map)
#     if (success):
#         response = {"status": "success"}
#     else:
#         response = {"status": "failed"}
#     # jsonfy volta o json para o usuário
#     return jsonify(response), 200

# @app.route('/find_student_by_id/<int:id>', methods=['GET'])
# def find_student_by_id(id):
#     student = academic_services.find_student_by_id(id)
#     if (student):
#         return student.jsonify(), 200
#     else:
#         return {"status": "not found"}, 404
    


if __name__ == '__main__':
    app.run(debug=True)
    

