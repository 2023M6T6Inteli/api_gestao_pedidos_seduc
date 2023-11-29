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

    for map in SUPPLIERS_MAPS:
        with SupplierDAO() as mng:
            mng.create_supplier(map)

    for map in TRANSPORTERS_MAPS:
        with TransporterDAO() as mng:
            mng.create_transporter(map)
    
    for map in SCHOOLS_MAPS:
        with SchoolDAO() as mng:
            mng.create_school(map)

    for map in EMPLOYES_SEDUC_MAPS:
        with EmployeSeducDAO() as mng:
            mng.create_employe_seduc(map)

    for map in EMPLOYES_TRANSPORTER_MAPS:
        with EmployeTransporterDAO() as mng:
            mng.create_employe_transporter(map)

    for map in EMPLOYES_SCHOOL_MAPS:
        with EmployeSchoolDAO() as mng:
            mng.create_employe_school(map)

    for map in EMPLOYES_SUPPLIER_MAPS:
        with EmployeSupplierDAO() as mng:
            mng.create_employe_supplier(map)

    for map in ORDERS_MAPS:
        with OrderDAO() as mng:
            mng.create_order(map)
    


if (__name__=="__main__"):
    main()
