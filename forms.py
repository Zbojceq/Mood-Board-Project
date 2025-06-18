from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.widgets import ListWidget, ColorInput, Select, TimeInput, DateInput, TextArea
from lists import emoticons_list
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
    emoticon = SelectField('Emoticon', widget=Select(),
                            choices=emoticons_list)
    color = StringField('Color', widget=ColorInput(), validators=[DataRequired()])
    submit = SubmitField('Create Emoticon')

class CalendarLogForm(FlaskForm):
    log_date = DateField("Log Date", widget=DateInput(), validators=[DataRequired()])   # Format: YYYY-MM-DD
    log_time = TimeField("Log Time", widget=TimeInput(), validators=[DataRequired()]) # Format: HH:MM
    emotions = SelectField('Emotions', widget=Select(),
                            choices=emotions_list, validators=[DataRequired()])
    description = StringField('Description', widget=TextArea(), validators=[DataRequired(), Length(min=1, max=200)])
    submit = SubmitField('Add Event')
 

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
