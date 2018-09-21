import requests
import json
import sys
from flaskrepositorio import db
from flaskrepositorio.models import User, Subject, SubjectClass, Course
import logging

BASE_URL = "http://sharashami.com/"

def sync(login):
    logging.basicConfig(level=logging.DEBUG)
    try:
        r = requests.get(BASE_URL + "student/" + str(login))
        if r.status_code == 200:
            content = r.json()
            save_user(content)
            save_subject_classes(content)
    except Exception as e:
        print(e, file=sys.stderr)

        

def save_user(content):
    user = User()
    user.id = content["_id"]
    user.name = content["name"]
    user.email = content["email"]
    user.login = content["enrollment_id"]
    db.session.add(user)


def save_course(content):
    course = Course()
    course.id = content["_id"]
    course.name = content["description"]
    db.session.add(course)


def save_subject(content, id_course):
    subject = Subject()
    subject.id = content["_id"]
    subject.name = content["description"]
    subject.course_id = id_course
    db.session.add(subject)


def save_subject_class(content, subject_id):
    save_course(content["program"])
    save_subject(content["course"])
    subject_class = SubjectClass()
    subject_class.id = content["_id"]
    subject_class.subject_id = content["course"]["_id"]
    db.session.add(subject_class)


def save_subject_classes(content):
    classes = content["classes"]
    for c in classes:
        save_subject_class(c)
        db.session.commit()

