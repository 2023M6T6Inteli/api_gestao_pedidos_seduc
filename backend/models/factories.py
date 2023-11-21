class StudentDAOFactory:
    """
    Creates a dao
    """
    def create(session):
        from .student import StudentDAO
        return StudentDAO(session)

class CourseDAOFactory:
    """
    Creates a dao
    """
    def create(session):
        from .course import CourseDAO
        return CourseDAO(session)