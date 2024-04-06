import argparse
import datetime
from models import Teacher, Group, Student, Subject, Grade
from connect import session




# Teacher
def create_teacher(session, name):
    teacher = Teacher(name=name)
    session.add(teacher)
    session.commit()
    session.close()

def list_teachers(session):
    teachers = session.query(Teacher).all()
    for teacher in teachers:
        print(f"{teacher.id} - {teacher.name}")
    session.close()

def update_teacher(session, teacher_id, name):
    teacher = session.query(Teacher).get(teacher_id)
    if teacher:
        teacher.name = name
        session.commit()
    session.close()

def remove_teacher(session, teacher_id):
    teacher = session.query(Teacher).get(teacher_id)
    if teacher:
        session.delete(teacher)
        session.commit()
    session.close()

# Group
def create_group(session, name):
    group = Group(name=name)
    session.add(group)
    session.commit()

def list_groups(session):
    groups = session.query(Group).all()
    for group in groups:
        print(f"ID: {group.id}, Name: {group.name}")

def update_group(session, group_id, name):
    group = session.query(Group).get(group_id)
    if group:
        group.name = name
        session.commit()

def delete_group(session, group_id):
    session.query(Group).filter(Group.id == group_id).delete()
    session.commit()


# Student
def create_student(session, name, group_id):
    student = Student(name=name, group_id=group_id)
    session.add(student)
    session.commit()

def list_students(session):
    students = session.query(Student).all()
    for student in students:
        print(f"ID: {student.id}, Name: {student.name}, Group ID: {student.group_id}")

def update_student(session, student_id, name, group_id):
    student = session.query(Student).get(student_id)
    if student:
        student.name = name
        student.group_id = group_id
        session.commit()

def delete_student(session, student_id):
    session.query(Student).filter(Student.id == student_id).delete()
    session.commit()

# Grade
def create_grade(session, student_id, subject_id, grade, date):
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    grade = Grade(student_id=student_id, subject_id=subject_id, grade=grade, date=date_obj)
    session.add(grade)
    session.commit()

def list_grades(session):
    grades = session.query(Grade).all()
    for grade in grades:
        print(f"ID: {grade.id}, Student ID: {grade.student_id}, Subject ID: {grade.subject_id}, Grade: {grade.grade}, Date: {grade.date}")

def update_grade(session, grade_id, student_id, subject_id, grade, date):
    grade_obj = session.query(Grade).get(grade_id)
    if grade_obj:
        grade_obj.student_id = student_id
        grade_obj.subject_id = subject_id
        grade_obj.grade = grade
        grade_obj.date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        session.commit()

def delete_grade(session, grade_id):
    session.query(Grade).filter(Grade.id == grade_id).delete()
    session.commit()

# Subjects
def create_subject(session, name, teacher_id):
    teacher = session.query(Teacher).get(teacher_id)
    if teacher:
        new_subject = Subject(name=name, teacher_id=teacher_id)
        session.add(new_subject)
        session.commit()
        print(f"Subject '{name}' added with Teacher ID: {teacher_id}")
    else:
        print("Teacher not found.")

def list_subjects(session):
    subjects = session.query(Subject).all()
    for subject in subjects:
        print(f"ID: {subject.id}, Name: {subject.name}, Teacher ID: {subject.teacher_id}")

def update_subject(session, subject_id, name=None, teacher_id=None):
    subject = session.query(Subject).get(subject_id)
    if subject:
        if name:
            subject.name = name
        if teacher_id:
            subject.teacher_id = teacher_id
        session.commit()
        print(f"Subject with ID {subject_id} updated.")
    else:
        print("Subject not found.")

def remove_subject(session, subject_id):
    subject = session.query(Subject).get(subject_id)
    if subject:
        session.delete(subject)
        session.commit()
        print(f"Subject with ID {subject_id} removed.")
    else:
        print("Subject not found.")

def main():
    parser = argparse.ArgumentParser(description="University Database Management")
    # Common arguments
    parser.add_argument("-a", "--action", required=True, choices=['create', 'list', 'update', 'remove'],
                        help="CRUD actions: create, list, update, remove")
    parser.add_argument("-m", "--model", required=True, choices=['Teacher', 'Group', 'Student', 'Subject', 'Grade'],
                        help="Models: Teacher, Group, Student, Subject, Grade")

    # Arguments for name-based models (Teacher, Group, Student, Subject)
    parser.add_argument("-n", "--name", help="Name of the object")

    # Argument for identification of specific records
    parser.add_argument("--id", type=int, help="ID of the object to update/remove")

    # Arguments specific to the Grade model
    parser.add_argument("--student_id", type=int, help="Student ID for the grade")
    parser.add_argument("--subject_id", type=int, help="Subject ID for the grade")
    parser.add_argument("--grade", type=int, help="Grade to be added/updated")
    parser.add_argument("--date", help="Date when the grade was given, format: YYYY-MM-DD")

    # Arguments for models involving foreign keys
    parser.add_argument("--group_id", type=int, help="Group ID for Student/Subject")
    parser.add_argument("--teacher_id", type=int, help="Teacher ID for Subject")

    args = parser.parse_args()

    if args.model == "Teacher":
        if args.action == "create":
            create_teacher(session, args.name)
        elif args.action == "list":
            list_teachers(session)
        elif args.action == "update":
            update_teacher(session, args.id, args.name)
        elif args.action == "remove":
            remove_teacher(session, args.id)
        else:
            print("Invalid action")
    elif args.model == "Group":
        if args.action == "create":
            create_group(session, args.name)
        elif args.action == "list":
            list_groups(session)
        elif args.action == "update":
            update_group(session, args.id, args.name)
        elif args.action == "delete":
            delete_group(session, args.id)
        else:
            print("Invalid action")
    elif args.model == "Student":
        if args.action == "create":
            create_student(session, args.name, args.group_id)
        elif args.action == "list":
            list_students(session)
        elif args.action == "update":
            update_student(session, args.id, args.name, args.group_id)
        elif args.action == "delete":
            delete_student(session, args.id)
        else:
            print("Invalid action")
    elif args.model == "Grade":
        if args.action == "create":
            create_grade(session, args.student_id, args.subject_id, args.grade, args.date)
        elif args.action == "list":
            list_grades(session)
        elif args.action == "update":
            update_grade(session, args.id, args.student_id, args.subject_id, args.grade, args.date)
        elif args.action == "delete":
            delete_grade(session, args.id)
        else:
            print("Invalid action")
    elif args.model == "Subject":
        if args.action == "create":
            create_subject(session, args.name, args.teacher_id)
        elif args.action == "list":
            list_subjects(session)
        elif args.action == "update":
            update_subject(session, args.id, args.name, args.teacher_id)
        elif args.action == "remove":
            remove_subject(session, args.id)
        else:
            print("Invalid action")


if __name__ == "__main__":
    main()