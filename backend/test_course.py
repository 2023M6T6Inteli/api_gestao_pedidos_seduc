from models.course import *

course = None
with CourseDAO() as dao:
    course = dao.find_by_id(1)

for student in course.students():
    print(student.jsonify(indent=4))


