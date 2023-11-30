import logging
from db_resetter import drop_n_create_db
from samples import *
from models import *
import time

# Configuração do Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Recreate DB
    logger.info("Iniciando recriação do banco de dados...")
    drop_n_create_db()
    logger.info("Banco de dados recriado com sucesso.")

    # Enter Courses
    logger.info("Inserindo cursos...")
    for map in COURSES_MAPS:
        with CourseDAO() as dao:
            dao.create_course(map)
    logger.info("Cursos inseridos.")

    # Enter Students
    logger.info("Inserindo estudantes...")
    for map in STUDENTS_MAPS:
        with StudentDAO() as mng:
            mng.create_student(map)
    logger.info("Estudantes inseridos.")

    logger.info("Inserindo suppliers...")
    for map in SUPPLIERS_MAPS:
        logger.info("map supplier", map)
        with SupplierDAO() as mng:
            logger.info("entrou with")
            mng.create_supplier(map)
    logger.info("Suppliers inseridos.")


    logger.info("Inserindo transporters...")
    for map in TRANSPORTERS_MAPS:
        with TransporterDAO() as mng:
            mng.create_transporter(map)
    logger.info("Transporters inseridos.")
    
    logger.info("Inserindo schools...")
    for map in SCHOOLS_MAPS:
        with SchoolDAO() as mng:
            mng.create_school(map)
    logger.info("Schools inseridos.")
  
    logger.info("Inserindo employes_seduc...")
    for map in EMPLOYES_SEDUC_MAPS:
        with EmployeSeducDAO() as mng:
            mng.create_employe_seduc(map)
    logger.info("Employes_seduc inseridos.")
     

    logger.info("Inserindo employes_transporter...")
    for map in EMPLOYES_TRANSPORTER_MAPS:
        with EmployeTransporterDAO() as mng:
            mng.create_employe_transporter(map)
    logger.info("Employes_transporter inseridos.")


    logger.info("Inserindo employes_school...")
    for map in EMPLOYES_SCHOOL_MAPS:
        with EmployeSchoolDAO() as mng:
            mng.create_employe_school(map)
    logger.info("Employes_school inseridos.")
    
    logger.info("Inserindo employes_supplier...")
    for map in EMPLOYES_SUPPLIER_MAPS:
        with EmployeSupplierDAO() as mng:
            mng.create_employe_supplier(map)
    logger.info("Employes_supplier inseridos.")
        
    logger.info("Inserindo orders...")
    for map in ORDERS_MAPS:
        with OrderDAO() as mng:
            mng.create_order(map)
    logger.info("Orders inseridos.")
    


if (__name__=="__main__"):
    main()
