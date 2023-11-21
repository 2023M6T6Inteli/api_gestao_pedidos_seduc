from models.student import *

student = None
with StudentDAO() as dao:
    student = dao.find_by_id(1)

for course in student.courses():
    print(course.jsonify())
    


