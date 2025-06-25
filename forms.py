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
    log_date = DateField("Log Date", widget=DateInput(), validators=[DataRequired()])
    log_time = TimeField("Log Time", widget=TimeInput(), validators=[DataRequired()])
    emotions = SelectField('Emotions', widget=Select(),
                            choices=emotions_list, validators=[DataRequired()])
    description = StringField('Description', widget=TextArea(), validators=[DataRequired(), Length(min=1, max=200)])
    submit = SubmitField('Add Event')

class NotificationForm(FlaskForm):
    notification_time_morning = TimeField("Notification Morning", widget=TimeInput(), validators=[DataRequired()])
    notification_time_afternoon = TimeField("Notification Afternoon", widget=TimeInput(), validators=[DataRequired()])
    notification_time_evening = TimeField("Notification Evening", widget=TimeInput(), validators=[DataRequired()])
    notification_time_night = TimeField("Notification Night", widget=TimeInput(), validators=[DataRequired()])
    notification_enabled_morning = BooleanField('Enable Morning', default=False)
    notification_enabled_afternoon = BooleanField('Enable Afternoon', default=False)
    notification_enabled_evening = BooleanField('Enable Evening', default=False) 
    notification_enabled_night = BooleanField('Enable Night', default=False)     
    submit = SubmitField('Add Notification')
 

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
