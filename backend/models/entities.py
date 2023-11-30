# Este arquivo define as entidades e a estrutura do banco de dados.
# uma entidade é um objeto que representa um registro ou linha em seu banco de dados. 
# As entidades lidam com os detalhes brutos dos dados, enquanto os modelos os tornam mais acessíveis e práticos de usar
from datetime import datetime
import json, uuid
from sqlalchemy.ext.declarative import declarative_base
from models.order_status import OrderStatus
from sqlalchemy.orm import relationship, backref
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
    address = Column(String(50))
    cep = Column(String(30))
    cnpj = Column(String(30))

    employes = relationship("EmployeSchoolEntity", backref="school")
    orders = relationship("OrderEntity", backref="school")

class SupplierEntity(Base):
    __tablename__ = 'suppliers_tb'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    address = Column(String(50))
    cep = Column(String(30))
    cnpj = Column(String(30))

    employes = relationship("EmployeSupplierEntity", backref="supplier")
    orders = relationship("OrderEntity", backref="supplier")

class TransporterEntity(Base):
    __tablename__ = 'transporters_tb'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    address = Column(String(50))
    cep = Column(String(30))
    cnpj = Column(String(30))

    employes = relationship("EmployeTransporterEntity", backref="transporter")
    orders = relationship("OrderEntity", backref="transporter")

class OrderEntity(Base):
    __tablename__ = 'orders_tb'

    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey('suppliers_tb.id'))
    employe_seduc_id = Column(Integer, ForeignKey('employeseduc_tb.id'))
    school_id = Column(Integer, ForeignKey('schools_tb.id'))    
    transporter_id = Column(Integer, ForeignKey('transporters_tb.id'))
    nf = Column(String(30), nullable=True)
    nr = Column(String(30), nullable=True)
    purchase_date = Column(DateTime)
    delivery_date = Column(DateTime)
    status = Column(Enum(OrderStatus))
    amount = Column(Float)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.utcnow)
    deletedAt = Column(DateTime, nullable=True)

class AssesmentEntity(Base):
    __tablename__ = 'assessments_tb'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders_tb.id'))
    employe_school_id = Column(Integer, ForeignKey('employeschool_tb.id'))
    purchase_date = Column(DateTime)
    delivery_date = Column(DateTime)

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
    email = Column(String(30))
    password = Column(String(30))
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.utcnow)
    deletedAt = Column(DateTime, nullable=True)

class EmployeSeducEntity(UserEntity):
    __tablename__ = 'employeseduc_tb'

    id = Column(Integer, ForeignKey('users_tb.id'), primary_key=True)
    role = Column(String(30))
    celular = Column(String(30))
    orders = relationship("OrderEntity", backref="employe_seduc")

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




