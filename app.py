from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegisterForm, EmotionForm, CalendarLogForm
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')

app.config['SECRET_KEY'] = '123456789' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager() #implementuje moduł logowania 
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Czas trwania sesji
#csrf = CSRFProtect(app)  # Inicjalizacja CSRF Protect


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    calendar_logs = db.relationship('CalendarLog', backref='user', lazy=True)
    calendar_log_day_summaries = db.relationship('CalendarLogDaySummary', backref='user', lazy=True)
    emotions = db.relationship('Emotion', backref='user', lazy=True)

class CalendarLog(UserMixin, db.Model):
    __tablename__ = 'calendar_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    event_time = db.Column(db.Time, nullable=True)
    description = db.Column(db.String(255), nullable=False)
    emotions_logs = db.relationship('EmotionLog', backref='calendar_log', lazy=True)

class CalendarLogDaySummary(UserMixin, db.Model):
    __tablename__ = 'calendar_log_summaries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    emotions_logs = db.relationship('EmotionLogSummary', backref='calendar_log_day_summary', lazy=True)

class Emotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    emotion_description = db.Column(db.String(255), nullable=False)
    emotion_emoticon = db.Column(db.String(255), nullable=True)
    color = db.Column(db.String(255), nullable=False)

class EmotionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('calendar_logs.id'), nullable=False)
    emotion_description = db.Column(db.String(255), nullable=False)
    emotion_emoticon = db.Column(db.String(255), nullable=True)
    color = db.Column(db.String(255), nullable=False)

class EmotionLogSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('calendar_log_summaries.id'), nullable=False)
    emotion_description = db.Column(db.String(255), nullable=False)
    emotion_emoticon = db.Column(db.String(255), nullable=True)
    color = db.Column(db.String(255), nullable=False)


with app.app_context():
    db.create_all() 

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main'))
        flash('Invalid username or password')       
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2')
        new_user = User(username=form.username.data, password=hashed_password, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/check_username', methods=['POST'])
def check_username():
    username = request.json.get('username')
    exists = User.query.filter_by(username=username).first() is not None
    return jsonify({'exists': exists})

@app.route('/check_email', methods=['POST'])
def check_email():
    email = request.json.get('email')
    exists = User.query.filter_by(email=email).first() is not None
    return jsonify({'exists': exists})

@app.route('/add_test')
@login_required
def add_test():
    date_str = '16.05.2023'
    date = datetime.strptime(date_str, '%d.%m.%Y').date()
    time_str = '10:00'
    time = datetime.strptime(time_str, '%H:%M').time()
    new_log = CalendarLog(
        user_id=current_user.id, 
        event_date=date, 
        event_time=time, 
        description="Meeting with team")
    db.session.add(new_log)
    db.session.commit()
    return 'Test added!'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    for i in range(len(current_user.emotions)):
        print(f'Emotion: {current_user.emotions[i].emotion_description}, Emoticon: {current_user.emotions[i].emotion_emoticon}, Color: {current_user.emotions[i].color}')
    text = f'Hello, {current_user.username}!, {current_user.calendar_logs[0].event_date} {current_user.calendar_logs[0].event_time} {current_user.calendar_logs[0].description}'
    text2 = f'Hello, {current_user.emotions[4].color} {current_user.emotions[4].emotion_description} {current_user.emotions[4].emotion_emoticon}'
    return text2


@app.route('/')
@login_required
def hello_world():
    return 'Hello, World!'

@app.route('/start')
def start():
    return render_template('start.html')


@app.route('/quotes')
def quotes():
    return render_template('quotes.html')   

@app.route('/relation_stats')
def relation_stats():
    return render_template('relation_stats.html')   

@app.route('/friends')
def friends():
    return render_template('friends.html')  

@app.route('/relation_notifs')
def relation_notifs():
    return render_template('relation_notifs.html')  

@app.route('/avatar')
def avatar():
    return render_template('avatar.html')  

@app.route('/stats')
@login_required
def stats():
    return render_template('stats.html')

@app.route('/emotion_create', methods=['GET', 'POST'])
def emotion_create():
    form = EmotionForm()
    if form.validate_on_submit():
        description = form.name.data
        emoticon = form.emoticon.data
        color = form.color.data
        
        new_emotion = Emotion(
            user_id=current_user.id,
            emotion_description=description,
            emotion_emoticon=emoticon,
            color=color
        )
        db.session.add(new_emotion)
        db.session.commit()
        flash('Emotion created successfully!', 'success')
        return redirect(url_for('main'))
    else:
        flash('Please fill in all fields.', 'danger')
    return render_template('emotion_create.html', form=form)

@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    form=CalendarLogForm()
    if form.validate_on_submit():
        log_date = form.log_date.data
        log_time = form.log_time.data
        emotions = form.emotions.data
        description = form.description.data
        
        new_log = CalendarLog(
            user_id=current_user.id,
            event_date=log_date,
            event_time=log_time,
            description=description
        )
        db.session.add(new_log)
        db.session.commit()
        flash('Event added successfully!', 'success')
    return render_template('main.html', form=form )

@app.route('/daily')
@login_required
def daily():
    return render_template('daily.html')

@app.route('/side_menu')
def side_menu():
    return render_template('side_menu.html')

@app.route('/notifs')
@login_required
def notifs():
    return render_template('notifs.html')

@app.route('/emotion_add')
def emotion_add():
    return render_template('emotion_add.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')
