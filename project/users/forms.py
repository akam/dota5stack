from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional

class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    steamID = StringField('steamID', validators=[DataRequired()])
    mmr = StringField('mmr', validators=[DataRequired()])
    carry = BooleanField('carry', validators=[Optional()])
    support1 = BooleanField('support1', validators=[Optional()])
    support2 = BooleanField('support2', validators=[Optional()])
    offlane = BooleanField('offlane', validators=[Optional()])
    mid = BooleanField('mid', validators=[Optional()])
    password = PasswordField('password', validators=[Length(min=6)])

class EditForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    steamID = StringField('steamID', validators=[DataRequired()])
    carry = BooleanField('carry', validators=[Optional()])
    support1 = BooleanField('support1', validators=[Optional()])
    support2 = BooleanField('support2', validators=[Optional()])
    offlane = BooleanField('offlane', validators=[Optional()])
    mid = BooleanField('mid', validators=[Optional()])
    mmr = StringField('mmr', validators=[DataRequired()])
    discord = StringField('discord')
    password = PasswordField('password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class DeleteForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])