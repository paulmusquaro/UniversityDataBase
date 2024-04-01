import logging
import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Group, Teacher, Subject, Student, Grade

fake = Faker()

print(fake.name())

# Підключення до бази даних
engine = create_engine('postgresql://postgres:blah_blah_blah@localhost/witchcraft', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Додавання фейкових даних до вже створених таблиць
    # Додавання груп
    for _ in range(3):
        group = Group(name=fake.word())
        session.add(group)

    # Додавання викладачів
    for _ in range(3):
        teacher = Teacher(fullname=fake.name())
        session.add(teacher)

    session.commit()

    # Додавання предметів із вказівкою викладача
    teachers = session.query(Teacher).all()
    for teacher in teachers:
        for _ in range(2):
            subject = Subject(name=fake.word(), teacher_id=teacher.id)
            session.add(subject)

    session.commit()

    # Додавання студентів і оцінок
    groups = session.query(Group).all()
    for group in groups:
        for _ in range(10):
            student = Student(fullname=fake.name(), group_id=group.id)
            session.add(student)
            session.commit()
            for subject in group.students:
                for _ in range(3):
                    grade = Grade(student_id=student.id, subject_id=subject.id, grade=random.randint(0, 100), grade_date=fake.date_this_decade())
                    session.add(grade)

    session.commit()

except Exception as e:
    logging.error(e)
    session.rollback()
finally:
    session.close()