import flask, flask_login, flask_mail
from werkzeug.utils import secure_filename
from . import forms
from .forms import videos
import center_app
import os
from . import models
from .auth.models import User
from .auth.forms import RegistrationForm
from . import db, login_mgr, mail_mgr
from config import DevConfig
import datetime



main_blueprint=flask.Blueprint('main',__name__)




@main_blueprint.route("/",methods=['GET','POST'])
def index():
    global trial_days_left
    global frm
    global courses
    global start
    global end
    global maximum
    global registered
    global view_course
    registered=None
    frm=User.new_register
    trial_days_left=7
    if flask_login.current_user.is_authenticated:
            trial_days_left=flask_login.current_user.trial_days()

    courses=models.Course.query.all()
    if flask.request.method=="GET":
        start=0
        end=3
    if flask.request.method=="POST" and "contact_us" in flask.request.form:
        start=0
        end=3
        name=flask.request.form.get('name')
        email=flask.request.form.get('email')
        input_msg=flask.request.form.get('input_message')
        flask.flash("Your message has been sent successfully. Royal Project will contact you shortly.")
        msg = flask_mail.Message(subject="Royal Project",
                                     body="{} sent you a message.\n The message is: {}.\nThe return e-mail address is: {}".format(flask.request.form.get('name'),flask.request.form.get('input_message'),flask.request.form.get('email')) ,
                  sender=('ssyelenik@gmail.com'),
                  recipients=['ssyelenik@gmail.com'])
        mail_mgr.send(msg)

    else:
        name="Full Name"
        email="Email Address"
        input_msg="Your Message"

    maximum = len(courses)
    try:
        if end>maximum:
            end=maximum
    except:
        start=0
        end=3
        if end>maximum:
            end=maximum
    try:
        if view_course:
            pass
    except:
        view_course=courses[0]

    if flask.request.method=="POST":
        already_registered=False
        if "login" in flask.request.form:
            user = User.authenticate(
                flask.request.form.get('email'),
                flask.request.form.get('password')
            )
            if user is not None:
                flask.flash("Login successful", 'success')
                return flask.redirect(flask.url_for('main.index'))

            flask.flash("Wrong user mail or password", 'danger')

        if "view_course" in flask.request.form:
            view_course=models.Course.query.filter_by(id=flask.request.form.get('view_course')).first()

            return flask.render_template("/index.html",already_registerd=already_registered,name=name,input_msg=input_msg,email=email,trial_days_left=trial_days_left,courses=courses,frm=frm,view_course=view_course,start=start,end=end)


        if "P" in flask.request.form:
            start-=3
            if start<0:
                start=0
                end=3
            else:
                end=start+3

            if end>maximum:
                end=maximum
        if "0" in flask.request.form:
            start=0
            end=3
            if end>maximum:
                end=maximum
        if "4" in flask.request.form:
            start=3
            end=6
            if start>maximum:
                start=0
                end=3
                if end>maximum:
                    end=maximum
            if end>maximum:
                end=maximum
        if "8" in flask.request.form:
            start=6
            end=9
            if start>maximum:
                start=3
                end=6
                if end>maximum:
                    end=maximum
                if start>maximum:
                    start=0
                    end=3
                    if end>maximum:
                        end=maximum
        if "9" in flask.request.form:
            start=9
            end=12
            if start>maximum:
                start=6
                end=9
                if end>maximum:
                    end=maximum
                if start>maximum:
                    start=3
                    end=6
                    if end>maximum:
                        end=maximum
                    if start>maximum:
                        start=0
                        end=3
                        if end>maximum:
                            end=maximum
        if "12" in flask.request.form:
            start=12
            end=15
            if end>maximum:
                end=maximum
            if start>maximum:
                start=9
                end=12
                if end>maximum:
                    end=maximum
                if start>maximum:
                    start=6
                    end=9
                    if end>maximum:
                        end=maximum
                    if start>maximum:
                        start=3
                        end=6
                        if end>maximum:
                            end=maximum
                        if start>maximum:
                            start=0
                            end=3
                            if end>maximum:
                                end=maximum
        if "N" in flask.request.form:
            if not start+3>maximum:
                start+=3
                if end+3>maximum:
                    end=maximum
                else:
                    end+=3
        if "sign_up" in flask.request.form:
            class_id=flask.request.form['sign_up']
            class_obj=models.Class.query.filter_by(id=class_id).first()
            print(class_obj.type)
            print(flask_login.current_user.membership_status)
            registered=None
            for cl in flask_login.current_user.u_classes:
                if int(cl.id)==int(class_id):
                    registered="already_registered"
                    break

            if not registered=="already_registered":
                flask_login.current_user.u_classes.append(class_obj)
                db.session.commit()
                registered="success"

    return flask.render_template("/index.html",registered=registered,name=name,input_msg=input_msg,email=email,trial_days_left=trial_days_left,courses=courses,frm=frm,view_course=view_course,start=start,end=end)

@main_blueprint.route("/admin",methods=['GET','POST'])
def admin():

    return flask.render_template("/admin/admin.html")

@main_blueprint.route("/manage_user",methods=['GET','POST'])
def manage_user():
    form=forms.AdminUpdateUser()
    user_list=User.query.all()
    u_for_update=user_list[0]
    # form.select_user.choices=select_user_list
    message="none"
    if flask.request.method=="POST":
        message="none"

        if "switch_to_virtual" in flask.request.form:
            all_users=User.query.all()
            for u in all_users:
                u.membership_status="virtual"
                db.session.commit()
                message="updated"

        else:

            user_id=flask.request.form.get('update_user')

            u_for_update=User.query.filter_by(id=user_id).first()

            if "update" in flask.request.form:

                u_for_update.age=flask.request.form.get('age')
                u_for_update.membership_status=flask.request.form['membership_status']
                db.session.commit()
                print(u_for_update.age)
                message="updated"

            if "delete" in flask.request.form:
                if u_for_update.id==flask_login.current_user.id:
                    message="delete_self"
                else:
                    db.session.delete(u_for_update)
                    db.session.commit()
                    message="deleted"

        return flask.render_template("/admin/manage_user.html",form=form,user_list=user_list,u_for_update=u_for_update,message=message)
    return flask.render_template("/admin/manage_user.html",form=form,user_list=user_list,u_for_update=u_for_update,message=message)


@main_blueprint.route("/add_class",methods=['GET','POST'])
def add_class():
    form=forms.AdminAddClass()
    all_courses=models.Course.query.all()
    course_list=[]
    for c in all_courses:
        course_item=(c.id,c.name)
        course_list.append(course_item)
    form.choose_course.choices=course_list
    message="none"
    if flask.request.method=="POST":
        course_id=form.choose_course.data
        name=form.name.data
        start=form.start.data
        end=form.end.data
        days=form.days.data
        hours=form.hours.data
        gender=form.gender.data
        type=form.type.data
        class_obj=models.Class(course_id=course_id,name=name,start=start,end=end,days=days,hours=hours,gender=gender,type=type)
        db.session.add(class_obj)
        db.session.commit()
        message="added"
    return flask.render_template("/admin/add_class.html",form=form,message=message)

@main_blueprint.route("/add_video_to_class",methods=['GET','POST'])
def add_video_to_class():
    form=forms.AdminClassVideo()
    all_classes=models.Class.query.all()
    class_list=[]
    for c in all_classes:
        if c.type=="virtual":
            class_item=(c.id,c.name)
            class_list.append(class_item)
    form.name.choices=class_list
    message="none"
    if flask.request.method=="POST":
        class_id=form.name.data
        sequ_nb=form.sequ_nb.data
        video_obj=models.Video.query.filter_by(class_id=class_id)

        for v in video_obj:
            if sequ_nb==v.sequ_nb:
                override_video_id=v.id
                message="duplicates"
                break
        f=form.video.data
        filename=secure_filename(f.filename)
        basedir=os.path.abspath(os.path.dirname(__file__))
        path_name=os.path.join('static',filename)
        f.save(os.path.join(basedir,'static',filename))
        if message=="duplicates":
            override_video=models.Video.query.filter_by(id=override_video_id).first()
            override_video.video_filename=path_name
            db.session.commit()
        else:
            new_video=models.Video(class_id=class_id,sequ_nb=sequ_nb,video_filename=path_name)
            db.session.add(new_video)
            db.session.commit()
            message="added"
    return flask.render_template("/admin/add_video_to_class.html",form=form,message=message)


@main_blueprint.route("/manage_class",methods=['GET','POST'])
def manage_class():
    form=forms.AdminManageClass()
    all_classes=models.Class.query.all()
    class_list=[]
    for c in all_classes:
        class_item=(c.id,c.name)
        class_list.append(class_item)
    form.choose_class.choices=class_list
    message="none"
    if flask.request.method=="POST":
        if "find_class" in flask.request.form:
            class_id=form.choose_class.data
            class_obj=models.Class.query.filter_by(id=class_id).first()
            sdate=str(class_obj.start)
            syear=sdate[0:4]
            smonth=sdate[5:7]
            sday=sdate[8:10]
            startfmt=smonth+"/"+sday+"/"+syear
            edate=str(class_obj.end)
            eyear=edate[0:4]
            emonth=edate[5:7]
            eday=edate[8:10]
            endfmt=emonth+"/"+eday+"/"+eyear
            form.starttxt.data=startfmt
            form.endtxt.data=endfmt
            form.hours.data=class_obj.hours
            form.days.data=class_obj.days
            form.gender.data=class_obj.gender
            form.type.data=class_obj.type
        if "update" in flask.request.form:
            class_id=form.choose_class.data
            class_obj=models.Class.query.filter_by(id=class_id).first()
            if form.start.data is not None and form.end.data is not None:
                class_obj.start=form.start.data
                class_obj.end=form.end.data
                class_obj.days=form.days.data
                class_obj.hours=form.hours.data
                class_obj.gender=form.gender.data
                class_obj.type=form.type.data
                db.session.commit()
            if form.start.data is None and form.end.data is not None:
                class_obj.end=form.end.data
                class_obj.days=form.days.data
                class_obj.hours=form.hours.data
                class_obj.gender=form.gender.data
                class_obj.type=form.type.data
                db.session.commit()
            if form.start.data is not None and form.end.data is None:
                class_obj.start=form.start.data
                class_obj.days=form.days.data
                class_obj.hours=form.hours.data
                class_obj.gender=form.gender.data
                class_obj.type=form.type.data
                db.session.commit()
            if form.start.data is None and form.end.data is None:
                class_obj.days=form.days.data
                class_obj.hours=form.hours.data
                class_obj.gender=form.gender.data
                class_obj.type=form.type.data
                db.session.commit()
            message="updated"
        if "delete" in flask.request.form:
            class_id=form.choose_class.data
            class_obj=models.Class.query.filter_by(id=class_id).first()
            db.session.delete(class_obj)
            db.session.commit()
            message="deleted"
            all_classes=models.Class.query.all()
            form.choose_class.date=all_classes[0].id
            form.days.data=""
            form.hours.data=""
            form.gender.data="0"
            form.type.data="on-site"
    return flask.render_template("/admin/manage_class.html",form=form,message=message)

@main_blueprint.route("/add_course",methods=['GET','POST'])
def add_course():
    form=forms.AdminAddCourse()
    message="none"
    if flask.request.method=="POST":
        name=form.name.data
        description=form.description.data
        f=form.presentation_video.data
        filename=secure_filename(f.filename)
        basedir=os.path.abspath(os.path.dirname(__file__))
        path_name=os.path.join('static',filename)
        f.save(os.path.join(basedir,'static',filename))
        new_course=models.Course(name=name,description=description,presentation_video=path_name)
        db.session.add(new_course)
        db.session.commit()
        message="added"
    return flask.render_template("/admin/add_course.html", form=form,message=message)

@main_blueprint.route("/manage_course",methods=['GET','POST'])
def manage_course():
    form=forms.AdminManageCourse()
    all_courses=models.Course.query.all()
    course_list=[]
    for course in all_courses:
        course_item=(course.id,course.name)
        course_list.append(course_item)
    form.name.choices=course_list
    message="none"

    if flask.request.method=="POST":
        if "find_course" in flask.request.form:
            message="none"
            course_id=form.name.data
            course_obj=models.Course.query.filter_by(id=course_id).first()
            form.description.data=course_obj.description
        if "submit" in flask.request.form:

            course_id=form.name.data
            course_obj=models.Course.query.filter_by(id=course_id).first()
            new_description=form.description.data
            course_obj.description=new_description
            if not form.presentation_video_update.data==None:
                f=form.presentation_video_update.data
                filename=secure_filename(f.filename)
                basedir=os.path.abspath(os.path.dirname(__file__))
                path_name=os.path.join('static',filename)
                f.save(os.path.join(basedir,'static',filename))
                course_obj.presentation_video=path_name
            db.session.commit()
            message="updated"
    return flask.render_template("/admin/manage_course.html", form=form, message=message)


@main_blueprint.route("/user_class",methods=['GET','POST'])
def user_class():
    form=forms.AdminUserClass()
    all_courses=models.Course.query.all()
    all_users=User.query.all()
    course_list=[]
    for c in all_courses:
        course_item=(c.id,c.name)
        course_list.append(course_item)
    form.course.choices=course_list

    user_list=[]
    for u in all_users:
        user_item=(u.id,u.name)
        user_list.append(user_item)
    form.us.choices=user_list
    class_list=["None available"]
    message="none"
    if flask.request.method=="POST":
        if "show_classes" in flask.request.form:
            course_id=form.course.data
            course_obj=models.Course.query.filter_by(id=course_id).first()
            user_id=form.us.data
            user_obj=User.query.filter_by(id=user_id).first()
            class_list=[]
            for cl in course_obj.c_class:
                if cl.type==user_obj.membership_status and cl.gender==user_obj.gender:
                    class_info=(cl.id,cl.name,cl.start,cl.end)
                    class_list.append(class_info)
            if not class_list:
                class_list=["None available"]

        if "submit" in flask.request.form:
            class_id=flask.request.form.get('classes')
            user_id=form.us.data
            user_obj=User.query.filter_by(id=user_id).first()
            class_obj=models.Class.query.filter_by(id=class_id).first()

            registered="no"

            if class_obj is None:

                message="failure"
            else:
                for i in class_obj.c_user:

                    if int(i.id)==int(user_id):
                        registered="yes"
                if registered=="yes":
                    message="already_registered"
                else:
                    class_obj.c_user.append(user_obj)
                    db.session.commit()
                    message="success"
    return flask.render_template("/admin/user_class.html",form=form,class_list=class_list, message=message)

@main_blueprint.route("/virtual",methods=['GET','POST'])
def virtual():
    global courses
    global start
    global end
    global maximum
    global view_course
    courses=models.Course.query.all()
    if flask.request.method=="GET":
        start=0
        end=3
    if flask.request.method=="POST" and "contact_us" in flask.request.form:
        start=0
        end=3
    maximum = len(courses)
    try:
        if end>maximum:
            end=maximum
    except:
        start=0
        end=3
        if end>maximum:
            end=maximum
    try:
        if view_course:
            pass
    except:
        view_course=courses[0]
    if flask.request.method=="POST":
        if "view_course" in flask.request.form:
            view_course=models.Course.query.filter_by(id=flask.request.form.get('view_course')).first()
            return flask.render_template("/virtual.html",courses=courses,view_course=view_course,start=start,end=end)
        if "P" in flask.request.form:
            start-=3
            if start<0:
                start=0
                end=3
            else:
                end=start+3
            if end>maximum:
                end=maximum
        if "0" in flask.request.form:
            start=0
            end=3
            if end>maximum:
                end=maximum
        if "4" in flask.request.form:
            start=3
            end=6
            if start>maximum:
                start=0
                end=3
                if end>maximum:
                    end=maximum
            if end>maximum:
                end=maximum
        if "8" in flask.request.form:
            start=6
            end=9
            if start>maximum:
                start=3
                end=6
                if end>maximum:
                    end=maximum
                if start>maximum:
                    start=0
                    end=3
                    if end>maximum:
                        end=maximum
        if "9" in flask.request.form:
            start=9
            end=12
            if start>maximum:
                start=6
                end=9
                if end>maximum:
                    end=maximum
                if start>maximum:
                    start=3
                    end=6
                    if end>maximum:
                        end=maximum
                    if start>maximum:
                        start=0
                        end=3
                        if end>maximum:
                            end=maximum
        if "12" in flask.request.form:
            start=12
            end=15
            if end>maximum:
                end=maximum
            if start>maximum:
                start=9
                end=12
                if end>maximum:
                    end=maximum
                if start>maximum:
                    start=6
                    end=9
                    if end>maximum:
                        end=maximum
                    if start>maximum:
                        start=3
                        end=6
                        if end>maximum:
                            end=maximum
                        if start>maximum:
                            start=0
                            end=3
                            if end>maximum:
                                end=maximum
        if "N" in flask.request.form:
            if not start+3>maximum:
                start+=3
                if end+3>maximum:
                    end=maximum
                else:
                    end+=3
        if "watch_class" in flask.request.form:
            class_id=flask.request.form.get('watch_class')
            class_obj=models.Class.query.filter_by(id=class_id).first()

            return flask.render_template("/watch.html",class_obj=class_obj)
    return flask.render_template("/virtual.html",courses=courses,view_course=view_course,start=start,end=end)


@main_blueprint.route("/men",methods=['GET','POST'])
def men():
    return flask.render_template("/men.html")

@main_blueprint.route("/women",methods=['GET','POST'])
def women():
    return flask.render_template("/women.html")