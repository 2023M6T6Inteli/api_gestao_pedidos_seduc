from db_resetter import drop_n_create_db
from samples import *
from models import *

def main():
    # Recreate DB
    drop_n_create_db()

    # Enter Courses
    for map in COURSES_MAPS:
        with CourseDAO() as dao:
            dao.create_course(map)

    # Enter Students
    for map in STUDENTS_MAPS:
        with StudentDAO() as mng:
            mng.create_student(map)

if (__name__=="__main__"):
    main()
