import random
from faker import Faker
from datetime import datetime
from models import Group, Teacher, Subject, Student, Grade
from connect import SessionLocal


fake = Faker()
print(fake.name())
session = SessionLocal()


# Додавання груп
groups = ['Group A', 'Group B', 'Group C']
for group_name in groups:
    group = Group(name=group_name)
    session.add(group)

session.commit()

# Додавання викладачів
for _ in range(random.randint(3, 5)):
    teacher = Teacher(name=fake.name())
    session.add(teacher)

session.commit()

# Додавання предметів
subjects = ['Math', 'History', 'Biology', 'Physics', 'Chemistry', 'Literature', 'Art', 'Computer Science']
for i, subject_name in enumerate(subjects, 1):
    teacher_id = random.choice(session.query(Teacher.id).all())[0]
    subject = Subject(name=subject_name, teacher_id=teacher_id)
    session.add(subject)

session.commit()

# Додавання студентів і оцінок
for _ in range(random.randint(30, 50)):
    student_name = fake.name()
    group_id = random.choice(session.query(Group.id).all())[0]
    student = Student(name=student_name, group_id=group_id)
    session.add(student)
    session.flush()  # Студент отримає ID перед додаванням оцінок

    for subject_id in session.query(Subject.id).all():
        for _ in range(random.randint(0, 20)):  # Додавання 0-20 оцінок для кожного студента з кожного предмету
            grade_value = random.randint(10, 100)
            grade_date = fake.date_between("-4y", datetime.now())
            grade = Grade(student_id=student.id, subject_id=subject_id[0], grade=grade_value, date=grade_date)
            session.add(grade)

session.commit()
session.close()