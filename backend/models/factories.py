# Este arquivo define fábricas para DAOs específicos, como StudentDAOFactory e CourseDAOFactory.

# Padrão Factory: Este padrão é usado para criar objetos (neste caso, DAOs) sem expor a lógica de criação ao cliente. 
# Isso ajuda a manter o código mais modular e fácil de manter.

# DAOs Específicos: Embora não mostrado diretamente aqui, presume-se que existam classes como StudentDAO e CourseDAO que estendem 
# BaseDAO e fornecem funcionalidades específicas para alunos e cursos.

# DAO como um assistente pessoal para lidar com todas as suas interações com um banco de dados. Seu trabalho é gerenciar a conexão 
# com o banco de dados, executar consultas e operações, e cuidar da logística de acesso aos dados.
# Relação com Entidades e Modelos: O DAO geralmente trabalha diretamente com as entidades. Quando você quer salvar, atualizar, ler ou deletar
# informações do banco de dados, o DAO lida com essas tarefas usando entidades.


# existe para que você não tenha que construir um StudentDAO toda vez que precisar de um. 
# Assim como uma fábrica que faz brinquedos para você, a StudentDAOFactory faz StudentDAOs

# uma session é usada para gerenciar transações de banco de dados. 
# Ela representa uma "área de trabalho" para todas as operações de banco de dados que você realizará.
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
    
class SchoolDAOFactory:
    """
    Creates a dao
    """
    def create(session):
        from .school import SchoolDAO
        return SchoolDAO(session)
    
class SupplierDAOFactory:
    """
    Creates a dao
    """
    def create(session):
        from .supplier import SupplierDAO
        return SupplierDAO(session)
    
class TransporterDAOFactory:
    """
    Creates a dao
    """
    def create(session):
        from .transporter import TransporterDAO
        return TransporterDAO(session)
    
class EmployeSeducDAOFactory:
    """
    Creates a dao
    """
    def create(session):
        from .employe_seduc import EmployeSeducDAO
        return EmployeSeducDAO(session)

class EmployeSchoolDAOFactory:
    """
    Creates a dao
    """
    def create(session):
        from .employe_school import EmployeSchoolDAO
        return EmployeSchoolDAO(session)

class EmployeTransporterDAOFactory:
    """
    Creates a dao
    """
    def create(session):
        from .employe_transporter import EmployeTransporterDAO
        return EmployeTransporterDAO(session)

class EmployeSupplierDAOFactory:
    """
    Creates a dao
    """
    def create(session):
        from .employe_supplier import EmployeSupplierDAO
        return EmployeSupplierDAO(session)

class OrderDAOFactory:
    """
    Creates a dao
    """
    def create(session):
        from .order import OrderDAO
        return OrderDAO(session)
    

# class StatusComponenteConfirmarEntega:
#     """
#     Creates a dao
#     """
#     def create(session):
#         from .entities import StatusComponenteConfirmarEntegaDAO
#         return StatusComponenteConfirmarEntegaDAO(session)