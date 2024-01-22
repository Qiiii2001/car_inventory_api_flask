from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length,Email, NumberRange

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()

class UserRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Sign Up')

class CarForm(FlaskForm):
    make = StringField('Make', validators=[DataRequired(), Length(min=2, max=50)])
    model = StringField('Model', validators=[DataRequired(), Length(min=2, max=50)])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1900, max=2100)])
    submit = SubmitField('Submit')