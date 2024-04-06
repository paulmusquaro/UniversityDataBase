from sqlalchemy.orm import sessionmaker
from models import Group, Student, Teacher, Subject, Grade
from sqlalchemy import create_engine, func, desc
from connect import SessionLocal




# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    session = SessionLocal()
    result = session.query(Grade.student_id, func.avg(Grade.grade).label('average_grade'))\
        .group_by(Grade.student_id)\
        .order_by(func.avg(Grade.grade).desc())\
        .limit(5).all()
    session.close()
    return result


# 2. Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_id):
    session = SessionLocal()
    result = session.query(Grade.student_id)\
        .filter(Grade.subject_id == subject_id)\
        .group_by(Grade.student_id)\
        .order_by(func.avg(Grade.grade).desc())\
        .first()
    session.close()
    return result


# 3. Знайти середній бал у групах з певного предмета.
def select_3(subject_id):
    session = SessionLocal()
    result = session.query(Student.group_id, func.avg(Grade.grade))\
        .join(Grade, Grade.student_id == Student.id)\
        .filter(Grade.subject_id == subject_id)\
        .group_by(Student.group_id).all()
    session.close()
    return result


# 4. Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    session = SessionLocal()
    result = session.query(func.avg(Grade.grade)).scalar()
    session.close()
    return result


# 5. Знайти які курси читає певний викладач.
def select_5(teacher_id):
    session = SessionLocal()
    result = session.query(Subject.name).filter_by(teacher_id=teacher_id).all()
    session.close()
    return result


# 6. Знайти список студентів у певній групі.
def select_6(group_id):
    session = SessionLocal()
    result = session.query(Student.name).filter_by(group_id=group_id).all()
    session.close()
    return result


# 7. Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_id, subject_id):
    session = SessionLocal()
    result = session.query(Student.name, Grade.grade).join(Grade).filter(
        Student.group_id == group_id,
        Grade.subject_id == subject_id
    ).all()
    session.close()
    return result


# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_id):
    session = SessionLocal()
    result = session.query(func.avg(Grade.grade)).join(Subject).filter(
        Subject.teacher_id == teacher_id
    ).scalar()
    session.close()
    return result


# 9. Знайти список курсів, які відвідує певний студент.
def select_9(student_id):
    session = SessionLocal()
    result = session.query(Subject.name).join(Grade).filter(
        Grade.student_id == student_id
    ).distinct().all()
    session.close()
    return result


# 10. Список курсів, які певному студенту читає певний викладач.
def select_10(student_id, teacher_id):
    session = SessionLocal()
    result = session.query(Subject.name).join(Grade).filter(
        Grade.student_id == student_id,
        Subject.teacher_id == teacher_id
    ).distinct().all()
    session.close()
    return result


# Add_1. Середній бал, який певний викладач ставить певному студентові.
def select_add_01(teacher_id, student_id):
    session = SessionLocal()
    result = session.query(Teacher.name, func.round(func.avg(Grade.grade), 2)).filter(
        Teacher.id == Subject.teacher_id,
        Grade.subject_id == Subject.id, 
        Subject.teacher_id == teacher_id, 
        Grade.student_id == student_id
        ).group_by(Teacher.name).all()
    session.close()
    return result


# Add_2. Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_add_02(group_id, subject_id):
    session = SessionLocal()
    result = session.query(Student.name, Grade.grade).filter(
        Grade.student_id == Student.id, 
        Student.group_id == group_id,
        Grade.subject_id == subject_id
        ).order_by(desc(Grade.date)).limit(1).all()
    session.close()
    return result




if __name__ == "__main__":
    print("1.------------------------")
    print(select_1())
    print("2.------------------------")
    print(select_2(3))
    print("3.------------------------")
    print(select_3(3))
    print("4.------------------------")
    print(select_4())
    print("5.------------------------")
    print(select_5(1))
    print("6.------------------------")
    print(select_6(2))
    print("7.------------------------")
    print(select_7(2, 3))
    print("8.------------------------")
    print(select_8(1))
    print("9.------------------------")
    print(select_9(5))
    print("10.-----------------------")
    print(select_10(5, 1))
    print("                          ")

    print("-----Additional tasks-----")
    print("Add_1.--------------------")
    print(select_add_01(2, 5))
    print("Add_2.--------------------")
    print(select_add_02(2, 2))