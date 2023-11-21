# Flask App

from flask import Flask, request, jsonify
from service.academic_services import AcademicServices
import json

app = Flask(__name__)
academic_services = AcademicServices()

@app.route('/enroll_student', methods=['POST'])
def enroll_student():
    student_map = json.loads(request.data)
    #print(student_map)
    """
    {
        "ra": "RA001",
        "nome": "Jeff"
    }
    """
    # Passa o mapa para a camada de serviços
    success = academic_services.enroll_student(student_map)
    if (success):
        response = {"status": "success"}
    else:
        response = {"status": "failed"}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
