from . import db, login_mgr, mail_mgr
import flask_mail,flask


# class ModelMixin(db.Model):
#     class Meta:
#         abstract=True
#
#     id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(64))

from .auth.models import User,Role
class Course(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    description=db.Column(db.String)

    presentation_video=db.Column(db.String)

    c_class=db.relationship("Class",backref="registered")
    avg_rating=db.Column(db.Integer)
    num_ratings=db.Column(db.Integer)


    def add_class(self):
        pass



    def remove_class(self):
        pass


users_to_classes=db.Table("users_to_classes",
                          db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                          db.Column('class_id',db.Integer,db.ForeignKey('class.id'))
                          )

class Event(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    content=db.Column(db.String)


class EventPics(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    picture=db.Column(db.String)
    details=db.Column(db.String)
    date=db.Column(db.DateTime)
    type=db.Column(db.String)

    def destroy(self):
        pass


class Class(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)

    course_id=db.Column(db.Integer,db.ForeignKey('course.id'))
    instructor_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    start=db.Column(db.DateTime)
    end=db.Column(db.DateTime)
    gender=db.Column(db.String)
    days=db.Column(db.String)
    hours=db.Column(db.String)
    type=db.Column(db.String)
    c_user=db.relationship("User",secondary="users_to_classes",back_populates="u_classes", lazy='dynamic')
    c_video=db.relationship("Video",backref="class_video")

    def add_user(self):
        pass
    def remove_user(self):
        pass
    def add_comment(self):
        pass

    def add_rate(self):
        pass

class Video(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    video_filename=db.Column(db.String)
    sequ_nb=db.Column(db.Integer)
    class_id=db.Column(db.Integer,db.ForeignKey('class.id'))
    __table_args__=(db.UniqueConstraint('sequ_nb', 'class_id'),)