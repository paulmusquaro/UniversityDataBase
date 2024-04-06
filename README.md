# University Database
This project is a command-line application to manage a university database. It uses SQLAlchemy to interact with a PostgreSQL database, performing various CRUD (Create, Read, Update, Delete) operations on entities such as Students, Teachers, Subjects, Groups, and Grades.Utilizing SQLAlchemy for ORM and PostgreSQL for the database, it simplifies complex CRUD operations. Alembic is used for database migration, ensuring that database schemas are managed and version-controlled efficiently.

## Database Structure
The university database consists of the following entities:

- Group: Represents groups that students belong to. Attributes: `id`, `name`.

- Student: Represents students. Attributes: `id`, `name`, `group_id`. It has a foreign key to the Group.

- Teacher: Represents teachers. Attributes: `id`,`name`.

- Subject: Represents subjects that teachers teach. Attributes: `id`, `name`,`teacher_id`. It has a foreign key to Teacher.

- Grade: Represents students' grades. Attributes: `id`, `student_id`, `subject_id`, `grade`, `date`. It has foreign keys to Student and Subject.

# Setup and Running the Application
1. Run Docker Engine via opening Docker Desktop.

2. Activate Virtual Environment:

    ```
    poetry shell
    ```

    Dependencies:

    - SQLAlchemy for ORM.
    - Faker for generating fake data.
    - Alembic: Database migration.
    - PostgreSQL as the database.


3. Create Docker Container and PostgreSQL DataBase:
    ```
    make up
    ```
    - If you are using Windows, please [follow the link](https://youtu.be/taCJhnBXG_w?si=h1xJKuL0rxcxUifu) and add "make" to your PATH. Or, if you don't want to add "make", just open "Makefile" and copy the command you want.

4. Create tables in DataBase:
    
    ```
    make alem
    ```
5. Filling the Database:

    ```
    make fill
    ```
    This command will fill Groups, Teachers, Subjects, Students, and Grades with randomly generated data using the Faker library. Or, you can run `interface.py` and fill it yourself.

    Here are the types of arguments you can use (for `interface.py`):

    - -a, --action: CRUD actions: create, list, update, remove.
    - -m, --model: Models: Teacher, Group, Student, Subject, Grade.
    - And others related to the specific attributes of each model you can see use the --help.
    
   For example, to list all teachers:

    ```
    py interface.py -a list -m Teacher
    ```

6. Data selections:

```
make se
```
This command will run `DBselect.py`