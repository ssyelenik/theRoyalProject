import flask_wtf
import wtforms as wtf
import wtforms.validators as vald

class RegistrationForm(flask_wtf.FlaskForm):

    name     = wtf.StringField("Name", validators=[vald.DataRequired()])
    email    = wtf.StringField("Email", validators=[vald.DataRequired()])
    password = wtf.PasswordField("Password", validators=[vald.DataRequired()])
    confirm  = wtf.PasswordField("Confirm password", validators=[vald.EqualTo("password")])
    profile_pic=wtf.StringField("Profile Picture")
    role     = wtf.SelectField("Role",choices=[('User','User'),('Teacher','Teacher')])
    age =wtf.IntegerField("Age")
    gender=wtf.SelectField("Gender",choices=[(0,'Female'),(1,'Male')])
    submit   = wtf.SubmitField("Register")




class LoginForm(flask_wtf.FlaskForm):
    email    = wtf.StringField("Email", validators=[vald.DataRequired()])
    password = wtf.PasswordField("Password", validators=[vald.DataRequired()])

    submit   = wtf.SubmitField("Sign in")