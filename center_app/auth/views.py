import flask
import flask_login

from .. import db

from . import auth_blueprint
from .forms import RegistrationForm, LoginForm
from .models import User,Role


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if flask.request.method=="POST":
        role_obj=Role.query.filter_by(name=form.role.data).first()
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
            permission=role_obj,
            age=form.age.data,
            gender=form.gender.data,
            membership_status='unpaid'
                   )
        db.session.add(user)
        db.session.commit()
        flask.flash(f"Welcome {user.name}! You just registered. Please login.")
        User.new_register="registered"
        User.new_register="registered"
        return flask.redirect(flask.url_for('main.index'))
    else:
        print(form.errors)

    return flask.render_template("register.html", form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.email.data,
            form.password.data
        )
        if user is not None:
            flask.flash("Login successful", 'success')
            User.new_register="logged_in"
            return flask.redirect(flask.url_for('main.index'))

        flask.flash("Wrong user mail or password", 'danger')

    return flask.render_template('login.html', form=form)

@auth_blueprint.route("/profile")
def profile():
    role_obj=Role.query.filter_by(id=flask_login.current_user.my_role).first()
    role=role_obj.name
    return flask.render_template('profile.html',role=role)

@auth_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('main.index'))

