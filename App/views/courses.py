from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from App.models import Program, ProgramCourses

from.index import index_views

from App.controllers import (
    list_all_courses,
    create_course

)

course_views = Blueprint('course_views', __name__, template_folder='../templates')


@course_views.route('/course', methods = ["GET"])
def list_courses_json():
    course_list = list_all_courses()
    course_json = ([course.get_json() for course in course_list])

    return jsonify(course_json)

@course_views.route('/course', methods = ['POST'])
def new_course():
    data = request.json
    course = create_course(data['code'], 
                  data['name'], 
                  data['credits'], 
                  data['rating'], 
                  data['semester'], 
                  data['level'],
                  data['offered'],
                  data['prereqs'])
    return "Successfully Created course!"
