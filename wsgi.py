

import click, pytest, sys
import random
import csv
from flask import Flask
from flask.cli import with_appcontext, AppGroup


from App.models.EasyCoursePlanner import EasyCoursePlanner
from App.models.FastCoursePlanner import FastCoursePlanner
from App.models.ElectiveCoursePlanner import ElectiveCoursePlanner
from App.models.CoursePlanner import CoursePlanner
from App.models.programCourses import ProgramCourses

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( 
    create_user, 
    get_all_users_json, 
    get_all_users, 
    create_program,
    get_all_OfferedCodes,
    get_core_credits,
    createCoursesfromFile,
    get_course_by_courseCode,
    get_prerequisites,
    get_all_courses,
    create_programCourse,
    createCourseOffering,
    deleteCourseOffering,
    getCourseOfferingsByYearAndSemester,
    create_student,
    create_staff,
    get_program_by_name,
    get_all_programCourses,
    addCoursetoHistory,
    getCompletedCourses,
    addCourseToPlan,
    get_student_by_id,
    list_all_courses,
    get_all_programs,
    getProgramCoursesByType,
    getCoursePlan,
    getPlanCourses,
    create_CoursePlan
    )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    createCoursesfromFile('testData/courseData.csv')
    create_program("Testing", 30, 54, 9)
    create_student(816, "testpass", "test", "Testing")
    create_student(8160, "pass", "blank", "Testing")
    create_staff("staffpass","999", "staff")
    

    test1 = ["COMP1600",  "COMP1601", "COMP1602", "COMP1603", "COMP1604", "MATH1115", "INFO1600", "INFO1601",  "FOUN1101", "FOUN1105", "FOUN1301", "COMP3605", "COMP3606", "COMP3607", "COMP3608",]
    for c in test1:
        # grade = random.choice(['A', 'B', 'C', 'F1', 'F2', 'F3'])
        grade = 'A'
        addCoursetoHistory(816, c, grade)
    print('Student course history updated')

    # add courses to program
    file_path = "testData/test.txt"
    with open(file_path, 'r') as file:
        programName=""
        for i, line in enumerate(file):
            line = line.strip()
            if i ==0:
                programName = line
            else:
                course = line.split(',')
                create_programCourse(programName, course[0],int(course[1]))
    print('Program courses updated')
    
    # # add course offerings for semester 1 of the year 2023/2024
    # file_path1='testData/test2.txt'
    # with open(file_path1, 'r') as file:
    #     for i, line in enumerate(file):
    #         line = line.strip()
    #         createCourseOffering(line, "2023/2024", 1) 
    

    file_path = "testData/courseData.csv"
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                courseCode = row["courseCode"]
                semester = int(row["semster"])
                createCourseOffering(courseCode, "2023/2024", semester)
            print('Course offerings for 2023/2024 created')
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return False    

    print('Database initialized')
'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())


app.cli.add_command(user_cli) # add the group to the cli

'''
Student
'''
student_cli = AppGroup("student", help="Student object commands")

# Define the student create command
@student_cli.command("create", help="Creates a student")
@click.argument("student_id", type=str)
@click.argument("password", type=str)
@click.argument("name", type=str)
@click.argument("programName", type=str)
def create_student_command(student_id, password, name, programname):
    create_student(student_id, password, name, programname)

@student_cli.command("addCourse", help="Student adds a completed course to their history")
@click.argument("student_id", type=str)
@click.argument("code", type=str)
@click.argument("grade", type=str)
@click.pass_context
def addCourse(ctx, student_id, code, grade):
    addCoursetoHistory(student_id, code, grade)

addCourse.params = [
    click.Argument(["student_id"], type=str),
    click.Argument(["code"], type=str),
    click.Argument(["grade"], type=str)
]



@student_cli.command("getCompleted", help="Get all of a student completed courses")
@click.argument("student_id", type=str)
def completed(student_id):
    comp = getCompletedCourses(student_id)
    for c in comp:
        print(f'Course Code: {c.code}, Grade: {c.grade}')


# @student_cli.command("addCourseToPlan", help="Adds a course to a student's course plan")
# def courseToPlan():
#     student = get_student_by_id("816")
#     addCourseToPlan(student, "COMP2611")


# @student_cli.command("generate", help="Generates a course plan based on what they request")
# @click.argument("student_id", type=str)
# @click.argument("command", type=str)
# def generatePlan(student_id, command):
#     student = get_student_by_id(student_id)
#     courses = generator(student, command)
#     for c in courses:
#         print(c)

@student_cli.command("getcourseplan", help= "Get the specified courseplan for the student")
@click.argument("student_id", type=str)
@click.argument("academic_year", type=str)
@click.argument("semester", type=str)
def getcourseplan(student_id, academic_year, semester):
    plan = getCoursePlan(student_id, academic_year, semester)
    if plan:
        print(f'{plan.get_json()}')
    else:
        print(f'Course plan requested not found')


app.cli.add_command(student_cli)

'''
Staff Commands
'''
staff_cli = AppGroup('staff',help='testing staff commands')

@staff_cli.command("create",help="create staff")
@click.argument("id", type=str)
@click.argument("password", type=str)
@click.argument("name", type=str)
def create_staff_command(id, password, name): 
  newstaff=create_staff(password, id, name)
  print(f'Staff {newstaff.name} created')

# @staff_cli.command("addprogram",help='testing add program feature')
# @click.argument("name", type=str)
# @click.argument("core", type=int)
# @click.argument("elective", type=int)
# @click.argument("foun", type=int)
# def create_program_command(name,core,elective,foun):
#   newprogram=create_program(name,core,elective,foun)
#   if newprogram:
#     print(f'{newprogram.get_json()}')

@staff_cli.command("addprogramcourse",help='testing add program course feature')
@click.argument("programname", type=str)
@click.argument("coursecode", type=str)
@click.argument("type", type=int)
def add_program_requirements(programname,coursecode,type):
  response=create_programCourse(programname, coursecode, type)
  if response is ProgramCourses:
    print(f'{response.get_json()}')

@staff_cli.command("addcourseoffering",help='testing add courses offering feature')
@click.argument("code", type=str)
@click.argument("year", type=str)
@click.argument("sem", type=int)
def add_course_offering(code, year, sem):
  offering=createCourseOffering(code, year, sem)
  if offering:
    print(f'{offering.get_json()}')

@staff_cli.command("removecourseoffering",help='testing remove courses offering feature')
@click.argument("code", type=str)
@click.argument("year", type=str)
@click.argument("sem", type=int)
def remove_course_offering(code, year, sem):
  deleteCourseOffering(code, year, sem)

app.cli.add_command(staff_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("course", help="Run Course tests")
@click.argument("type", default="all")
def courses_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["App/tests/courses.py::CourseUnitTests"]))

    elif type == "int":
        sys.exit(pytest.main(["App/tests/courses.py::CourseIntegrationTests"]))

    else:
        sys.exit(pytest.main(["App/tests/courses.py"]))

@test.command("coursePlan", help="Run Course Plan tests")
@click.argument("type", default="all")
def course_plan_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["App/tests/coursePlan.py::CoursePlanUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["App/tests/coursePlan.py::CoursePlanIntegrationTests"]))
    else:
        sys.exit(pytest.main(["App/tests/coursePlan.py"]))
    
#CoursesOfferedPerSemUnitTests
@test.command("coursesOffered", help="Run Courses Offered Per Sem tests")
@click.argument("type", default="all")
def courses_offered_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["App/tests/coursesOfferedPerSem.py::CoursesOfferedPerSemUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["App/tests/coursesOfferedPerSem.py::CoursesOfferedPerSemIntegrationTests"]))
    else:
        sys.exit(pytest.main(["App/tests/coursesOfferedPerSem.py"]))
    

@test.command("program", help="Run Program tests")
@click.argument("type", default="all")
def program_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["App/tests/program.py::ProgramUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["App/tests/program.py::ProgramIntegrationTests"]))
    else:
        sys.exit(pytest.main(["App/tests/program.py"]))


@test.command("staff", help="Run Staff tests")
@click.argument("type", default="all")
def staff_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["App/tests/staff.py::StaffUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["App/tests/staff.py::StaffIntegrationTests"]))
    else:
        sys.exit(pytest.main(["App/tests/staff.py"]))

@test.command("student", help="Run Program tests")
@click.argument("type", default="all")
def student_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["App/tests/student.py::StudentUnitTest"]))
    elif type == "int":
        sys.exit(pytest.main(["App/tests/student.py::StudentIntegrationTests"]))
    else:
        sys.exit(pytest.main(["App/tests/student.py"]))

@test.command("studentCH", help="Run Student Course History tests")
@click.argument("type", default="all")
def student_history_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["App/tests/studentCourseHistory.py::CourseHistoryUnitTest"]))
    elif type == "int":
        sys.exit(pytest.main(["App/tests/studentCourseHistory.py::CourseHistoryIntegrationTests"]))
    else:
        sys.exit(pytest.main(["App/tests/studentCourseHistory.py"]))



app.cli.add_command(test)
#################################################################

'''
Program Commands
'''

program = AppGroup('program', help = 'Program object commands')

@program.command('create', help='Create a new program')
@click.argument('name', type=str)
@click.argument('core', type=int)
@click.argument('elective', type=int)
@click.argument('foun', type=int)
def create_program_command(name, core, elective, foun):
    newprogram=create_program(name,core,elective,foun)
    if newprogram:
        print(f'{newprogram.get_json()}')
    
@program.command("getprograms", help='Get all programs')
def get_programs():
    programs=get_all_programs()
    if programs:
        for program in programs:
            print(f'{program.get_json()}')

@program.command('core', help='Get program core courses')
@click.argument('programname', type=str)
def get_CoreCourses(programname):
    # create_programCourse("Computer Science Major", "COMP2611", 1)
    # create_programCourse("Computer Science Major", "COMP3605", 1)
    # create_programCourse("Computer Science Major", "COMP3610", 2)
    core = getProgramCoursesByType(programname, 1)
    for c in core:
        print({c.code})

@program.command('corecredits', help='Get program core courses')
@click.argument('programname', type=str)
def get_CoreCredits(programname):
    credits = get_core_credits(programname)
    print(f'Total Core Credits = {credits}') if credits else print(f'error')

@program.command('allcourses', help='Get all courses')
@click.argument('programname', type=str)
def allCourses(programname):
    all = get_all_courses(programname)
    for course in all:
        print(course.code)

@program.command('getprogram', help='Get a program by name')
@click.argument('programname', type=str)
def getProgram(programname):
   program = get_program_by_name(programname)
   print(f'{program.id}')

@program.command('addCourse', help='Add a course to a program')
@click.argument('programname', type=str)
@click.argument('code', type=str)
@click.argument('type', type=int)
def addProgramCourse(programname, code, type):
    c = create_programCourse(programname, code, type)
    if c:
        print(f'Course:{c.code} Type:{c.courseType}')

@program.command('getprogramCourses', help='Get all courses of a program')
@click.argument('programname', type=str)
def getProgramCourses(programname):
   courses = get_all_programCourses(programname)
   for c in courses:
       print(f'{c.code} {c.courseType}')

app.cli.add_command(program)
#################################################################

'''
Course Commands
'''
course = AppGroup('course', help = 'Course object related commands')

# @course.command('create', help='Create a new course')
# @click.argument('file_path')
# def create_course_command(file_path):  
#     newcourse = create_course(file_path)
#     print(f'Course created with course code "{newcourse.courseCode}", name "{newcourse.courseName}", credits "{newcourse.credits}", ratings "{newcourse.rating}" and prerequites "{newcourse.prerequisites}"')

@course.command('all', help = 'get all the courses in the db') 
def list_courses():
    print(list_all_courses())

@course.command('prereqs', help='Create a new course')
@click.argument('code', type=str)
def create_course_command(code):  
    prereqs = get_prerequisites(code)
    print(f'These are the prerequisites for {code}: {prereqs}') if prereqs else print(f'error')

@course.command('getcourse', help='Get a course by course code')
@click.argument('code', type=str)
def get_course(code):  
    course = get_course_by_courseCode(code)
    print(f'{course.get_json()}') if course else print(f'error')

@course.command('getprereqs', help='Get all prerequistes for a course')
@click.argument('code', type=str)
def get_course_prerequisites(code):  
    prereqs = get_prerequisites(code)
    for r in prereqs:
        print(f'{r.prereq_code}')

# @course.command('nextsem', help='Add a course to offered courses')
# @click.argument('code', type=str)
# def add_course(code):
#     course = addSemesterCourses(code)
#     print(f'Course Name: {course.courseName}') if course else print(f'error')

# @course.command('getNextSemCourses', help='Get all the courses offered next semester')
# def allSemCourses():
#     courses = get_all_OfferedCodes()

#     if courses:
#         for c in courses:
#             print({c})
#     else:
#         print("empty")
    
@course.command("offering", help='Get courses offerings for specified year and semester')
@click.argument("year", type=str)
@click.argument("sem", type=int)
def get_course_offering(year, sem):
  offerings=getCourseOfferingsByYearAndSemester(year, sem)
  if offerings:
    for offering in offerings:
        print(f'{offering.get_json()}')

app.cli.add_command(course)


#################################################################

'''
Course Plan Commands
'''

course_plan = AppGroup('course_plan', help = 'Course plan object related commands')

@course_plan.command('newPlan', help = 'create a new courseplan for a student')
@click.argument('id', type=int)
@click.argument('year', type = str)
@click.argument('sem', type = int)
def new_course_plan(id, year, sem):
    create_CoursePlan(id, year, sem)
    # print("Course plan created!")


@course_plan.command('getPlan', help = 'get a courseplan for a student')
@click.argument('id', type=int)
@click.argument('year', type = str)
@click.argument('sem', type = int)
def get_course_plan(id, year, sem):
    courseplan = getCoursePlan(id, year, sem)
    print (courseplan.get_json())


@course_plan.command('AddCourse', help = 'add a new course for a student')
@click.argument('id', type=int)
@click.argument('courseCode', type = str)
@click.argument('year', type = str)
@click.argument('sem', type = int)
def add_new_course(id, courseCode, year, sem):
    plan = addCourseToPlan(id, courseCode, year, sem)
    if (plan):
        print(plan.get_json())
    else:
        print("no success")

@course_plan.command('getplancourses', help = "get a list of courses in the course plan") 
@click.argument('student_id', type = int)
@click.argument('year', type = str)
@click.argument('sem', type = int)
def get_plan_courses(student_id, year, sem):
    plan_courses = getPlanCourses(student_id, year, sem)
    for plan in plan_courses:
        print(plan.get_json())
    # print(getPlanCourses(student_id))


app.cli.add_command(course_plan)


'''
Course Plan Generator Commands
'''

generate = AppGroup('generate', help = 'Generate a course plan based on strategy selected')

@generate.command('createplan', help = 'Generate a course plan based on strategy selected')
@click.argument('student_id', type=int)
@click.argument('strategy', type=str)
@click.argument('year', type=str)
def generate_plan(student_id, strategy, year):
    if strategy.lower() == "easy":
        strategy = EasyCoursePlanner()
        params = [student_id]
    elif strategy.lower() == "elective":
        electives = input("Please enter the electives you wish to pursue (e.g. COMP3606, COMP3607): ")
        strategy = ElectiveCoursePlanner() 
        params = [student_id, year, electives]
    elif strategy.lower() == "fast":
        strategy = FastCoursePlanner()
        params = [student_id, year]
    else:
        print("Invalid planning strategy. Please choose 'easy', 'fast' or 'elective'.")
        return

    context = CoursePlanner(strategy)
    result = context.plan_courses(params)

   
@generate.command("easyplan")
@click.argument('student_id', type = int)
def easyplantest(student_id):
    strategy = EasyCoursePlanner()
    context = CoursePlanner(strategy)
    result = context.plan_courses(student_id)








app.cli.add_command(generate)