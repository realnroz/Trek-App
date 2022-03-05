
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     PasswordField)
from wtforms.validators import DataRequired,EqualTo,Length,Regexp,Email

class RegistrationForm(FlaskForm):
    first_name=StringField('First Name',validators=[DataRequired()])
    last_name=StringField('Last Name',validators=[DataRequired()])
    address=StringField('Address',validators=[DataRequired()])
    phone_number=StringField('Phone Number',validators=[DataRequired(),Regexp(regex='^[0-9]{10}$',message="Invalid phone number.")])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password1=PasswordField('Password',validators=[DataRequired(),EqualTo('password2',message='Passwords do not match.')])
    password2=PasswordField('Confirm Password',validators=[DataRequired()])
