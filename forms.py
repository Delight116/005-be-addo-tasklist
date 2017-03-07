from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField, PasswordField, HiddenField, TextAreaField, validators , ValidationError
import datetime



class LoginForm(FlaskForm):
    nikname = StringField('Nikname', [validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=6, message="Min length 6 symbols")
    ])

class RegistrationForm(FlaskForm):
    nikname = StringField('Nikname', [validators.DataRequired('Must be more than 3 and symbol'), validators.Length(min=3, max=25)])
    firstname = StringField('Firstname', [validators.DataRequired()])
    lastname = StringField('Lastname', [validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=3, max=25),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class TaskForm(FlaskForm):
    user_id = HiddenField('user id')
    title = StringField('title', [validators.DataRequired(), validators.Length(max=70)])
    task = TextAreaField('Task', [validators.Length(max=256)])
    date = DateField('Date', [validators.DataRequired()], format='%d.%m.%Y', default= datetime.datetime.today()+datetime.timedelta(days=0))
    date_to = DateField('Date to', [validators.DataRequired()], format='%d.%m.%Y', default=datetime.datetime.today() + datetime.timedelta(days=1))
    status = BooleanField('Done')