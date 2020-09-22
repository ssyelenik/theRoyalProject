from flask_wtf import FlaskForm
import wtforms
from datetime import datetime
from flask_wtf.file import FileField,FileAllowed,FileRequired
from flask_uploads import UploadSet, ALL, IMAGES

videos=UploadSet('videos',ALL)

class AdminUpdateUser(FlaskForm):

    select_user=wtforms.SelectField("Select User to Update")

    role     = wtforms.SelectField("Role",choices=[('User','User'),('Teacher','Teacher')])
    age =wtforms.IntegerField("Age")
    gender=wtforms.SelectField("Gender",choices=[(0,'Female'),(1,'Male')])
    membership_status=wtforms.SelectField("Membership Status",choices=[('unpaid','Unpaid'),('on-site','On Site'),('virtual','Virtual')])
    update   = wtforms.SubmitField("Update")
    delete   = wtforms.SubmitField("Delete")
    switch_to_virtual=wtforms.SubmitField("Switch All to Virtual Membership")

class AdminAddCourse(FlaskForm):
    name=wtforms.StringField("Course Name")
    description=wtforms.TextAreaField("Course Description",render_kw={"rows": 5, "cols": 35})
    presentation_video=FileField("Presentation Video",validators=[FileAllowed(videos, 'Videos only!'), FileRequired('File was empty!')])
    submit=wtforms.SubmitField("Add Course")

class AdminManageCourse(FlaskForm):
    name=wtforms.SelectField("Course Name")
    description=wtforms.TextAreaField("Course Description",render_kw={"rows": 5, "cols": 35})
    presentation_video_update=FileField("New Presentation Video",validators=[FileAllowed(videos, 'Videos only!'), FileRequired('File was empty!')])
    submit=wtforms.SubmitField("Update Course")
    find_course=wtforms.SubmitField("Find Course")

class AdminUserClass(FlaskForm):
    us=wtforms.SelectField("User")
    course=wtforms.SelectField("Course")
    show_classes=wtforms.SubmitField("Show Available Classes")
    submit=wtforms.SubmitField("Register User to Class")

class AdminAddClass(FlaskForm):
    choose_course=wtforms.SelectField("Course to Associate with your Class")
    name=wtforms.StringField("Class Name")
    start=wtforms.DateField("Class Start Date", format='%m/%d/%Y')
    end=wtforms.DateField("Class End Date", format='%m/%d/%Y')
    gender=wtforms.SelectField("Gender the Class is Intended For", choices=[("0","Women/Girls"),("1","Men/Boys")])
    type=wtforms.SelectField("Type of Class",choices=[("virtual","virtual"),("on-site","on-site")])
    days=wtforms.StringField("Days")
    hours=wtforms.StringField("Hours")
    submit=wtforms.SubmitField("Add Class")

class AdminManageClass(FlaskForm):
    choose_class=wtforms.SelectField("Choose Class to Update")
    find_class=wtforms.SubmitField("Find Class")
    name=wtforms.StringField("Class Name")
    start=wtforms.DateField("New Start Date", format='%m/%d/%Y')
    starttxt=wtforms.StringField("Start Date")
    end=wtforms.DateField("New End Date", format='%m/%d/%Y')
    endtxt=wtforms.StringField("End Date")
    gender=wtforms.SelectField("Gender the Class is Intended For", choices=[("0","Women/Girls"),("1","Men/Boys")])
    type=wtforms.SelectField("Type of Class",choices=[("virtual","virtual"),("on-site","on-site")])
    days=wtforms.StringField("Days")
    hours=wtforms.StringField("Hours")
    update=wtforms.SubmitField("Update Class")
    delete=wtforms.SubmitField("Delete Class")

class AdminClassVideo(FlaskForm):
    name=wtforms.SelectField("Add Videos to This Virtual Class")

    video=FileField("New Presentation Video",validators=[FileAllowed(videos, 'Videos only!'), FileRequired('File was empty!')])
    sequ_nb=wtforms.IntegerField("Enter the Video Sequence Number")
    submit=wtforms.SubmitField("Add Video")

