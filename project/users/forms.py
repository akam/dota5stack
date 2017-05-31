from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    steamID = StringField('steamID', validators=[DataRequired()])
    mmr = StringField('mmr', validators=[DataRequired()])
    password = PasswordField('password', validators=[Length(min=6)])

class EditForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    steamID = StringField('steamID', validators=[DataRequired()])
    mmr = StringField('mmr', validators=[DataRequired()])
    discord = StringField('discord')
    password = PasswordField('password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class DeleteForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])