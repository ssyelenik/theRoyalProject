import flask_login
from flask_login import UserMixin
from .. import db, login_mgr
from sqlalchemy.sql import func
import datetime

@login_mgr.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    permission=db.relationship('User',backref='permission')

# First - Create a class that inherit from db.Model
from center_app import models
class User(UserMixin,db.Model):
    new_register="new"
    # Second - Create your model's columns
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    email    = db.Column(db.String(132))
    password = db.Column(db.String(512))
    profile_pic=db.Column(db.String)
    role    = db.Column(db.Integer,db.ForeignKey('role.id'))
    age=db.Column(db.Integer)
    gender=db.Column(db.String)
    membership_status=db.Column(db.String)
    date_joined= db.Column(db.DateTime(timezone=True), server_default=func.now())
    u_interests=db.relationship("Interest",secondary="user_interests",back_populates="i_user")
    u_classes=db.relationship("Class",secondary="users_to_classes",back_populates="c_user")
    u_comments=db.relationship("Comment",secondary="user_comments",back_populates="c_user")

    def trial_days(self):
        delta=datetime.datetime.now()-self.date_joined
        days_left=7-delta.days
        print(days_left)
        if int(days_left)==0:
            return -1
        else:
            return days_left

    def set_password(self, pwd):
        self.password = pwd

    def check_password(self, pwd):
        return self.password == pwd

    def send_reset_pwd_mail(self):
            payload = {
                'user_id': self.id,
                'expires': (datetime.datetime.now() + datetime.timedelta(hours=2)).timestamp()
            }

            token = jwt.encode(payload, app.config["SECRET_KEY"])

            url = flask.url_for('main.reset_password', jwt_token=token, _external=True)
            # Create a mail
            msg = flask_mail.Message(
                subject="Password Reset",
                recipients=[self.email],
                body=f"Hello {self.name}, to reset your password, navigate to {url}",
                sender=app.config["MAIL_USERNAME"]
            )

            # Send it !
            mail_mgr.send(msg)

    @classmethod
    def authenticate(cls, mail, password):
        user = cls.query.filter_by(email=mail).first()
        if user is not None and user.check_password(password):
            flask_login.login_user(user)
            return user


    def __repr__(self):
        return f"<User {self.name}>"

    def apply_for_course(self):
        pass

    def send_mail(self):
        pass

    def send_activation_mail(self):
        pass


class Interest(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    i_user=db.relationship("User",secondary="user_interests",back_populates="u_interests")

user_interests=db.Table("user_interests",
                          db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                          db.Column('interest_id',db.Integer,db.ForeignKey('interest.id'))
                          )

class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    text=db.Column(db.String)
    c_user=db.relationship("User",secondary="user_comments",back_populates="u_comments")

user_comments=db.Table("user_comments",
                          db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                          db.Column('comment_id',db.Integer,db.ForeignKey('comment.id'))
                          )

