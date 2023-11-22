# Este arquivo define as entidades e a estrutura do banco de dados.
# uma entidade é um objeto que representa um registro ou linha em seu banco de dados. 
# As entidades lidam com os detalhes brutos dos dados, enquanto os modelos os tornam mais acessíveis e práticos de usar
import datetime
import json, uuid
from sqlalchemy.ext.declarative import declarative_base
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

from backend.models.order_status import OrderStatus

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

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    address = Column(String)
    cep = Column(String)

    employes = relationship("EmployeSchoolEntity", back_populates="school")

class SupplierEntity(Base):
    __tablename__ = 'suppliers_tb'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    supplier_name = Column(String)
    cnpj = Column(String)
    rate = Column(Integer)

    employes = relationship("EmployeSupplierEntity", back_populates="supplier")

class TransporterEntity(Base):
    __tablename__ = 'transporters_tb'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    supplier_id = Column(String, ForeignKey('suppliers_tb.id'))
    name = Column(String)

    employes = relationship("EmployeTransporterEntity", back_populates="transporter")

class OrderEntity(Base):
    __tablename__ = 'orders_tb'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    supplier_id = Column(String, ForeignKey('suppliers_tb.id'))
    employe_seduc_id = Column(String, ForeignKey('employeseduc_tb.id'))
    school_id = Column(String, ForeignKey('schools_tb.id'))
    transporter_id = Column(String, ForeignKey('transporters_tb.id'), nullable=True)
    nf = Column(String, nullable=True)
    nr = Column(String, nullable=True)
    shipment_date = Column(DateTime)
    status = Column(Enum(OrderStatus))
    amount = Column(Float)

class AssesmentEntity(Base):
    __tablename__ = 'assessments_tb'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, ForeignKey('orders_tb.id'))
    employe_school_id = Column(String, ForeignKey('employeschool_tb.id'))
    shipment_date = Column(DateTime)

class StudentEntity(Base):
    __tablename__ = "students_tb"

    id = Column(Integer, primary_key=True)
    ra = Column(String(10), nullable=False)
    name = Column(String(200), nullable=False)

    courses = relationship(
        "CourseEntity",
        secondary=students_courses_tb,
        back_populates='students'
    )

class CourseEntity(Base):
    __tablename__ = "courses_tb"

    id = Column(Integer, primary_key=True)
    code = Column(String(10), nullable=False)
    name = Column(String(200), nullable=False)

    students = relationship(
        "StudentEntity",
        secondary=students_courses_tb,
        back_populates='courses'
    )


# Entity Users Models
# ==============================================================================


class UserEntity(Base):
    __tablename__ = 'users_tb'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    cpf = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, onupdate=datetime.utcnow)
    deletedAt = Column(DateTime, nullable=True)

class EmployeSeducEntity(UserEntity):
    __tablename__ = 'employeseduc_tb'

    id = Column(String, ForeignKey('users_tb.id'), primary_key=True)
    role = Column(String)
    celular = Column(String)

class EmployeSchoolEntity(UserEntity):
    __tablename__ = 'employeschool_tb'

    id = Column(String, ForeignKey('users_tb.id'), primary_key=True)
    school_id = Column(String, ForeignKey('schools_tb.id'), unique=True)

class EmployeSupplierEntity(UserEntity):
    __tablename__ = 'employesupplier_tb'

    id = Column(String, ForeignKey('users_tb.id'), primary_key=True)
    supplier_id = Column(String, ForeignKey('suppliers_tb.id'), unique=True)

class EmployeTransporterEntity(UserEntity):
    __tablename__ = 'employetransporter_tb'

    id = Column(String, ForeignKey('users_tb.id'), primary_key=True)
    transporter_id = Column(String, ForeignKey('transporters_tb.id'), unique=True)
    celular = Column(String)




