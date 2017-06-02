from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional

class TeamForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    prefix = StringField('name', validators=[Length(max=10)])