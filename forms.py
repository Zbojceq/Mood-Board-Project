from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.widgets import ListWidget, ColorInput, Select
from lists import emotions_list


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=150)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login', render_kw={"class": "login"})

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    email = StringField('Email', validators=[DataRequired(), Length(min=6, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=150)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register', render_kw={"class": "register"})

class EmotionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=150)])
    emoticon = SelectField('Emoticon', widget=Select(), validators=[DataRequired()],
                            choices=emotions_list)
    color = StringField('Color', widget=ColorInput(), validators=[DataRequired()])
    submit = SubmitField('Create Emoticon')


def validate_username(self, username):
    from app import User  # Import User model here to avoid circular import issues
    from app import db  # Import db here to avoid circular import issues
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError('Username already exists. Please choose a different one.')
        
def validate_email(self, email):
    from app import User  # Import User model here to avoid circular import issues
    from app import db  # Import db here to avoid circular import issues
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError('Email already exists. Please choose a different one.')
