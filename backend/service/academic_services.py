from models.student import StudentDAO
from models.course import CourseDAO

class AcademicServices:

    def enroll_student(self, student_map):
        with StudentDAO() as dao:
            dao.create_student(student_map)        
        return True

    def create_course(self, course_map):
        with CourseDAO() as dao:
            dao.create_course(course_map)
        return True



