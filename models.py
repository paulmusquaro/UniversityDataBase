import logging
from datetime import datetime
from sqlalchemy import ForeignKey, String, create_engine, Integer, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy.exc import DatabaseError
from sqlalchemy_utils import create_database, database_exists


class Base(DeclarativeBase):
    pass

class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(150), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"))
    group: Mapped["Group"] = relationship(back_populates="students")
    grades: Mapped["Grade"] = relationship(back_populates="student")

class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(150), nullable=False)

class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(175), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"))
    teacher: Mapped["Teacher"] = relationship(back_populates="subjects")


class Grade(Base):
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(175), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"))
    grade: Mapped[int] = mapped_column(CheckConstraint("grade >= 0 AND grade <= 100"))
    grade_date: Mapped[datetime] = mapped_column(nullable=False)


def create_all_tables(engine):
    """Create tables in the database."""
    Base.metadata.create_all(engine)


def create_table(session, table_class):
    """Create a table from the provided SQLAlchemy table class."""
    try:
        session.execute(table_class.__table__.create(bind=engine))
        session.commit()
    except DatabaseError as e:
        logging.error(e)
        session.rollback()


if __name__ == '__main__':

    connection_string = "postgresql://postgres:blah_blah_blah@localhost/witchcraft"
    engine = create_engine(connection_string)

    if not database_exists(engine.url):
        create_database(engine.url)

    DBSession = sessionmaker(bind=engine)

    with DBSession() as session:
        create_all_tables(engine)

        try:
            table_classes = [Group, Student, Teacher, Subject, Grade]
            for table_class in table_classes:
                if not table_class:
                    create_table(session, table_class)
                else:
                    logging.info("Table '%s' already exists, skipping creation.", table_class.__tablename__)
        except RuntimeError as err:
            logging.error(err)