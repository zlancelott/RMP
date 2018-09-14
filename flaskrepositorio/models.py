from flaskrepositorio import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserClassAssociation(db.Model):
    __tablename__ = 'user_class'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    subject_class_id = db.Column(db.Integer, db.ForeignKey('subject_class.id'), primary_key=True)
    is_mod = db.Column(db.Boolean)
    user = db.relationship("User", back_populates="subject_classes")
    subject_class = db.relationship("SubjectClass", back_populates="users")


lesson_file_topic_table = db.Table('lesson_file_topic', db.Model.metadata,
                                   db.Column('lesson_file_id', db.Integer, db.ForeignKey('lesson_file.id')),
                                   db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'))
                                   )


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(30), nullable=False)
    subjects = db.relationship("Subject", back_populates="course")

    def __repr__(self):
        return f"Course('{self.name}', '{self.code}')"


class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(30), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship("Course", back_populates="subjects")
    subject_classes = db.relationship("SubjectClass", back_populates="subject")
    topics = db.relationship("Topic", back_populates="subject")

    def __repr__(self):
        return f"Subject('{self.name}', '{self.code}')"


class SubjectClass(db.Model, UserMixin):
    __tablename__ = 'subject_class'
    id = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.String(10), nullable=False)
    code = db.Column(db.String(30), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship("Subject", back_populates="subject_classes")
    lessons = db.relationship("Lesson", back_populates="subject_class")
    users = db.relationship("UserClassAssociation", back_populates="subject_class")

    def __repr__(self):
        return f"SubjectClass('{self.code}', '{self.semester}')"


class Lesson(db.Model):
    __tablename__ = 'lesson'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    subject_class_id = db.Column(db.Integer, db.ForeignKey('subject_class.id'))
    subject_class = db.relationship("SubjectClass", back_populates="lessons")
    lesson_files = db.relationship("LessonFile", back_populates="lesson")

    def __repr__(self):
        return f"Lesson('{self.date}')"


class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship("Subject", back_populates="topics")
    lesson_files = db.relationship(
        "LessonFile",
        secondary=lesson_file_topic_table,
        back_populates="topics")
    
    def __repr__(self):
        return f"Topic('{self.name}')"


class LessonFile(db.Model):
    __tablename__ = 'lesson_file'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    lesson = db.relationship("Lesson", back_populates="lesson_files")
    topics = db.relationship(
        "Topic",
        secondary=lesson_file_topic_table,
        back_populates="lesson_files")
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship("User", foreign_keys=[author_id])
    reviewer = db.relationship("User", foreign_keys=[reviewer_id])

    def __repr__(self):
        return f"LessonFile('{self.name}', '{self.author}')"


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    subject_classes = db.relationship("UserClassAssociation", back_populates="user")

    def __repr__(self):
        return f"User('{self.login}', '{self.name}')"
