import logging
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Group, Teacher, Subject, Student, Grade

# Підключення до бази даних
engine = create_engine('postgresql://postgres:blah_blah_blah@localhost/witchcraft', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    result = session.query(Grade.student_id, func.avg(Grade.grade).label('avg_grade')).\
        group_by(Grade.student_id).\
        order_by(func.avg(Grade.grade).desc()).\
        limit(5).all()
    print(result)

    # Знайти студента із найвищим середнім балом з певного предмета.
    result = session.query(Grade.student_id, func.avg(Grade.grade).label('avg_grade')).\
        filter(Grade.subject_id == 2).\
        group_by(Grade.student_id).\
        order_by(func.avg(Grade.grade).desc()).\
        limit(1).all()
    print(result)

    # Знайти середній бал у групах з певного предмета.
    result = session.query(Group.id, func.avg(Grade.grade)).\
        join(Student, Group.id == Student.group_id).\
        join(Grade, Student.id == Grade.student_id).\
        filter(Grade.subject_id == 2).\
        group_by(Group.id).all()
    print(result)

    # Знайти середній бал на потоці (по всій таблиці оцінок)
    result = session.query(func.avg(Grade.grade)).scalar()
    print(result)

    # Знайти які курси читає певний викладач.
    result = session.query(Subject.name).filter(Subject.teacher_id == 3).all()
    print(result)

    # Знайти список студентів у певній групі.
    result = session.query(Student.fullname).filter(Student.group_id == 3).all()
    print(result)

    # Знайти оцінки студентів у окремій групі з певного предмета.
    result = session.query(Grade.grade).join(Student).filter(Student.group_id == 2, Grade.subject_id == 2).all()
    print(result)

    # Знайти середній бал, який ставить певний викладач зі своїх предметів.
    result = session.query(func.avg(Grade.grade)).\
        join(Subject, Grade.subject_id == Subject.id).\
        filter(Subject.teacher_id == 2).scalar()
    print(result)

    # Список курсів, які відвідує студент.
    result = session.query(Subject.name).\
        join(Grade, Grade.subject_id == Subject.id).\
        filter(Grade.student_id == 2).all()
    print(result)

    # Список курсів, які певний студент читає певному викладачу.
    result = session.query(Subject.name).\
        join(Grade, Grade.subject_id == Subject.id).\
        filter(Grade.student_id == 4, Subject.teacher_id == 2).all()
    print(result)

except Exception as e:
    logging.error(e)
finally:
    session.close()