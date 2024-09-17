from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from App.models import Program, ProgramCourses




from.index import index_views

from App.controllers import (
    create_user,
    create_program,
    create_programCourse,
    jwt_authenticate, 
    get_all_users,
    get_all_users_json,
    jwt_required,
    get_all_OfferedCodes,
    get_all_programCourses,
    verify_staff,
    createCourseOffering,
    deleteCourseOffering,
    getAllCourseOfferings,
    getCourseOfferingsByYearAndSemester,
    get_program_by_name,
    list_all_courses,
    create_course
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/staff/offeredCourses', methods=['GET'])
@login_required
def getOfferedCourses():
  username=current_user.username
  if not verify_staff(username):    #verify that the user is staff
    return jsonify({'message': 'You are unauthorized to perform this action. Please login with Staff credentials.'}), 401

  # listing=get_all_OfferedCodes()
  # listing = getAllCourseOfferings()
  # offered_json = ([course.get_json() for course in listing])
  # return jsonify(offered_json), 200
  course_list = list_all_courses()
  course_json = ([course.get_json() for course in course_list])

  return jsonify(course_json)





@staff_views.route('/staff/offeredCourses/yearsem', methods=['GET'])
@login_required
def getOfferedCoursesYearSem():
  data = request.json
  year = data['year']
  sem = data['sem']

  username=current_user.username
  if not verify_staff(username):    #verify that the user is staff
    return jsonify({'message': 'You are unauthorized to perform this action. Please login with Staff credentials.'}), 401

  # listing=get_all_OfferedCodes()
  listing = getCourseOfferingsByYearAndSemester(year, sem)
  offered_json = ([course.get_json() for course in listing])
  return jsonify(offered_json), 200


  

@staff_views.route('/staff/program', methods=['POST'])
@login_required
def addProgram():
  data=request.json
  name=data['name']
  core=data['core']
  elective=data['elective']
  foun=data['foun']

  username=current_user.username
  if not verify_staff(username):    #verify that the user is staff
    return jsonify({'message': 'You are unauthorized to perform this action. Please login with Staff credentials.'}), 401

  # get all programs and check to see if it already exists
  programs=get_program_by_name(name)
  # programNames=[]
  # for p in programs:
  #   programNames.append(p.name)
  # if name in programNames:
  if programs:
    return jsonify({'message': 'Program already exists'}), 400
  
  if not isinstance(core, int):
            return jsonify({"error": "'core' must be an integer"}), 400
  
  if not isinstance(elective, int):
            return jsonify({"error": "'elective' must be an integer"}), 400

  if not isinstance(foun, int):
            return jsonify({"error": "'foun' must be an integer"}), 400

  newprogram = create_program(name, core, elective, foun)
  if newprogram:
    return jsonify({'message': f"Program {newprogram.name} added"}), 200 
  else:
     return jsonify({'message': "Program creation unsucessful"}), 400


@staff_views.route('/programRequirement', methods=['POST'])
@login_required
def addProgramRequirements():
  data=request.json
  name=data['name']
  code=data['code']
  num=data['type']

  username=current_user.username
  if not verify_staff(username):    #verify that the user is staff
    return jsonify({'message': 'You are unauthorized to perform this action. Please login with Staff credentials.'}), 401

  #verify program existance 
  programs=Program.query.all()
  programNames=[]
  for p in programs:
    programNames.append(p.name)
  if name not in programNames:
    return jsonify({'message': 'Program does not exist'}), 400
  
  #verify that the course isn't already a requirement
  courseList=get_all_programCourses(name)
  courseCodeList=[]
  for c in courseList:
    courseCodeList.append(c.code)
  
  code=code.replace(" ","").upper()
  if code in courseCodeList:
    return jsonify({'message': f'{code} is already a requirement for {name}'}), 400

  #verify that the course type is valid; Core (1) Elective (2) Foundation (3)
  if num<1 or num>3:
    return jsonify({'message': 'Invalid course type. Core (1) Elective (2) Foundation (3)'}), 400

  response=create_programCourse(name, code, num)
  return jsonify({'message': response.get_json()}), 200


# @staff_views.route('/staff/addOfferedCourse', methods=['POST'])
# @login_required
# def addCourse():
#   data=request.json
#   courseCode=data['code']

#   username=current_user.username
#   if not verify_staff(username):    #verify that the user is staff
#     return jsonify({'message': 'You are unauthorized to perform this action. Please login with Staff credentials.'}), 401

#   offeredCourses=get_all_OfferedCodes()
#   courseCode=courseCode.replace(" ","").upper()   #ensure consistent course code format

#   #check if course code is already in the list of offered courses
#   if courseCode in offeredCourses:
#     return jsonify({'message': f"{courseCode} already exists in the list of offered courses"}), 400

#   course = addSemesterCourses(courseCode)
#   if course:
#      return jsonify(course.get_json()), 200
#   else:
#     return jsonify({'message': "Course addition unsucessful"}), 400





@staff_views.route('/staff/addOfferedCourse', methods=['POST'])
@login_required
def addCourseOffering():
  data=request.json
  courseCode=data['code']
  year = data['year']
  sem = data['sem']

  username=current_user.username
  if not verify_staff(username):    #verify that the user is staff
    return jsonify({'message': 'You are unauthorized to perform this action. Please login with Staff credentials.'}), 401

  offering = createCourseOffering(courseCode, year, sem)
  if offering is not None:
     return jsonify(offering.get_json()), 200
  else:
    return jsonify({'message': "Course offering creation unsucessful"}), 400





@staff_views.route('/staff/removeCourseOffering', methods=['DELETE'])
@login_required
def removeCourseOffering():
  data=request.json
  courseCode=data['code']
  year = data['year']
  sem = data['sem']
  courseCode=courseCode.replace(" ","").upper()   #ensure consistent course code format

  username=current_user.username
  if not verify_staff(username):    #verify that the user is staff
    return jsonify({'message': 'You are unauthorized to perform this action. Please login with Staff credentials.'}), 401

  deleted = deleteCourseOffering(courseCode, year, sem)
  if deleted:
     return jsonify({'message:': "Course offering deletion succesful"}), 200
  else:
    return jsonify({'message': "Course offering deletion unsucessful"}), 404
  



@staff_views.route('/staff/createcourse', methods=['POST'])
@login_required
def new_course():
  data = request.json

  username=current_user.username
  if not verify_staff(username):    #verify that the user is staff
    return jsonify({'message': 'You are unauthorized to perform this action. Please login with Staff credentials.'}), 401


  course = create_course(data['code'], 
                data['name'], 
                data['credits'], 
                data['rating'], 
                data['semester'], 
                data['level'],
                data['offered'],
                data['prereqs'])
  return jsonify("Successfully Created course!")