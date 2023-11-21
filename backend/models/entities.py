import json
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