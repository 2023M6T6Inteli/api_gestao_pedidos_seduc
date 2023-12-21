# Este arquivo define as entidades e a estrutura do banco de dados.
# uma entidade é um objeto que representa um registro ou linha em seu banco de dados. 
# As entidades lidam com os detalhes brutos dos dados, enquanto os modelos os tornam mais acessíveis e práticos de usar

from datetime import datetime
import json, uuid
from sqlalchemy.ext.declarative import declarative_base
from models.order_status import OrderStatus
from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    Float,
    Date,
    DateTime,
    Text,
    Enum,
    Boolean,
    Table,
    UniqueConstraint,
    ForeignKey
)

# Criação do banco de dados
Base = declarative_base()

# Association Tables
# ==============================================================================
students_courses_tb = Table(
    "students_courses_tb",
    Base.metadata,
    Column("student_id", ForeignKey("students_tb.id")),
    Column("course_id", ForeignKey("courses_tb.id"), nullable=False),
)

# Entity Models
# ==============================================================================

class SchoolEntity(Base):
    __tablename__ = 'schools_tb'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    address = Column(String(60))
    cep = Column(String(30))
    cnpj = Column(String(30))

    employes = relationship("EmployeSchoolEntity", backref="school", lazy='noload')
    orders = relationship("OrderEntity", backref=backref("school_orders", lazy='noload'), lazy='noload')

class SupplierEntity(Base):
    __tablename__ = 'suppliers_tb'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    address = Column(String(50))
    cep = Column(String(30))
    cnpj = Column(String(30))

    employes = relationship("EmployeSupplierEntity", backref="supplier", lazy='noload')
    orders = relationship("OrderEntity", backref=backref("supplier_orders", lazy='noload'), lazy='noload')


class TransporterEntity(Base):
    __tablename__ = 'transporters_tb'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    address = Column(String(50))
    cep = Column(String(30))
    cnpj = Column(String(30))

    employes = relationship("EmployeTransporterEntity", backref="transporter", lazy='noload')
    orders = relationship("OrderEntity", backref=backref("transporter_orders", lazy='noload'), lazy='noload')

# class TransporterEntity(Base):
#     __tablename__ = 'transporters_tb'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50))
#     address = Column(String(50))
#     cep = Column(String(30))
#     cnpj = Column(String(30))

#     employes = relationship("EmployeTransporterEntity", backref="transporter")
#     orders = relationship("OrderEntity", backref="transporter")

class OrderEntity(Base):
    __tablename__ = 'orders_tb'

    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey('suppliers_tb.id'))
    employe_seduc_id = Column(Integer, ForeignKey('employeseduc_tb.id'))
    school_id = Column(Integer, ForeignKey('schools_tb.id'))
    transporter_id = Column(Integer, ForeignKey('transporters_tb.id'), nullable=True)
    nf = Column(String(30), nullable=True)
    nr = Column(String(30), nullable=True)
    purchase_date = Column(DateTime)
    delivery_date = Column(DateTime)
    status = Column(Enum(OrderStatus))
    amount = Column(Float)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.utcnow)
    deletedAt = Column(DateTime, nullable=True)

    supplier = relationship("SupplierEntity", backref=backref("orders_supplier", lazy='noload'), lazy='joined')
    employe_seduc = relationship("EmployeSeducEntity", backref=backref("orders_employe_seduc", lazy='noload'), lazy='joined')
    school = relationship("SchoolEntity", backref=backref("orders_school", lazy='noload'), lazy='joined')
    transporter = relationship("TransporterEntity", backref=backref("orders_transporters", lazy='noload'), lazy='joined')

# class StatusComponenteConfirmarEntregaEntity(Base):
#     __tablename__ = 'status_componente_confirmar_entrega_tb'
#     id = Column(Integer, primary_key=True)
#     status = Column(Boolean, nullable=False)




# class AssesmentEntity(Base):
#     __tablename__ = 'assessments_tb'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     order_id = Column(Integer, ForeignKey('orders_tb.id'))
#     employe_school_id = Column(Integer, ForeignKey('employeschool_tb.id'))
#     purchase_date = Column(DateTime)
#     delivery_date = Column(DateTime)

class StudentEntity(Base):
    __tablename__ = "students_tb"

    id = Column(Integer, primary_key=True)
    ra = Column(String(30), nullable=False)
    name = Column(String(50), nullable=False)

    courses = relationship(
        "CourseEntity",
        secondary=students_courses_tb,
        back_populates='students'
    )

class CourseEntity(Base):
    __tablename__ = "courses_tb"

    id = Column(Integer, primary_key=True)
    code = Column(String(30), nullable=False)
    name = Column(String(50), nullable=False)

    students = relationship(
        "StudentEntity",
        secondary=students_courses_tb,
        back_populates='courses'
    )


# Entity Users Models
# ==============================================================================


class UserEntity(Base):
    __tablename__ = 'users_tb'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    cpf = Column(String(50), unique=True)
    email = Column(String(50))
    password = Column(String(30))
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.utcnow)
    deletedAt = Column(DateTime, nullable=True)

class EmployeSeducEntity(UserEntity):
    __tablename__ = 'employeseduc_tb'

    id = Column(Integer, ForeignKey('users_tb.id'), primary_key=True)
    role = Column(String(30))
    celular = Column(String(30))
    orders = relationship("OrderEntity", backref=backref("employe_seduc_orders", lazy='noload'), lazy='noload')

class EmployeSchoolEntity(UserEntity):
    __tablename__ = 'employeschool_tb'

    id = Column(Integer, ForeignKey('users_tb.id'), primary_key=True)
    school_id = Column(Integer, ForeignKey('schools_tb.id'), unique=True)

class EmployeSupplierEntity(UserEntity):
    __tablename__ = 'employesupplier_tb'

    id = Column(Integer, ForeignKey('users_tb.id'), primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers_tb.id'), unique=True)

class EmployeTransporterEntity(UserEntity):
    __tablename__ = 'employetransporter_tb'

    id = Column(Integer, ForeignKey('users_tb.id'), primary_key=True)
    transporter_id = Column(Integer, ForeignKey('transporters_tb.id'), unique=True)
    celular = Column(String(30))



# Imagine que você tem um álbum de figurinhas (sua tabela principal) e algumas figurinhas têm links para outros pequenos álbuns (suas tabelas relacionadas). Agora, vamos ver como esses diferentes métodos do SQLAlchemy funcionam, usando a analogia das figurinhas:

# Eager Loading:

# Imagina que, toda vez que você pega uma figurinha, automaticamente pega os pequenos álbuns relacionados a ela. Isso é como o eager loading – ele carrega as figurinhas e os pequenos álbuns relacionados de uma vez.
# Joinedload:

# É um tipo de eager loading. Imagine que você está pegando uma figurinha e, ao mesmo tempo, todas as figurinhas dos pequenos álbuns relacionados são coladas na parte de trás dela. Assim, você tem tudo em uma única página.
# Selectinload:

# Outro tipo de eager loading. Desta vez, você pega sua figurinha principal e, em seguida, separadamente, mas rapidamente, pega todos os pequenos álbuns relacionados. É um pouco mais organizado do que o joinedload.
# Lazy='noload':

# Aqui, quando você pega uma figurinha, decide não olhar os pequenos álbuns relacionados. Mesmo que haja um link, você ignora. Isso é útil quando você sabe que não precisa desses álbuns pequenos.
# Subquery:

# É uma forma de carregar as informações dos pequenos álbuns de forma mais eficiente, fazendo uma consulta separada para cada álbum, mas tudo em uma só vez.
# Lazy='dynamic':

# Imagine que, em vez de pegar todas as figurinhas dos pequenos álbuns de uma vez, você tem uma máquina mágica que pega as figurinhas para você quando pede. Esse método só pega as figurinhas dos pequenos álbuns quando você realmente precisa delas.
