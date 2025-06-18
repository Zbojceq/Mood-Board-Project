from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegisterForm, EmotionForm, CalendarLogForm
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from collections import Counter, defaultdict

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
    emotion_color = db.Column(db.String(255), nullable=False)
    emotion_description = db.Column(db.String(255), nullable=False)
    emotion_emoticon = db.Column(db.String(255), nullable=True)

class Emotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def hello_user():
    return redirect(url_for('main'))


#THESE ARE FOR TESTING, ITS LEFT HERE FOR FUTURE TEST PURPOSES
'''
@app.route('/dashboard')
@login_required
def dashboard():
    for i in range(len(current_user.emotions)):
        print(f'Emotion: {current_user.emotions[i].emotion_description}, Emoticon: {current_user.emotions[i].emotion_emoticon}, Color: {current_user.emotions[i].color}')
    for i in range(len(current_user.calendar_logs)):
        print(f'Log {i}: {current_user.calendar_logs[i].event_date} {current_user.calendar_logs[i].event_time} {current_user.calendar_logs[i].description} {current_user.calendar_logs[i].emotion_color} {current_user.calendar_logs[i].emotion_description} {current_user.calendar_logs[i].emotion_emoticon}')
    return 

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


'''



####### THESE ARE NOT IMPLEMENTED 
'''
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
'''





@app.route('/stats')
@login_required
def stats():
    logs = CalendarLog.query.filter_by(user_id=current_user.id).all()
    if not logs:
        return render_template('stats.html', stats_available=False)
    mood_counter = Counter((log.emotion_description, log.emotion_emoticon, log.emotion_color) for log in logs)
    most_common_moods = mood_counter.most_common(3)
    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_emotions = defaultdict(list)

    for log in logs:
        if log.event_date and log.emotion_description:
            weekday = log.event_date.weekday()
            weekday_emotions[weekday].append((log.emotion_description, log.emotion_emoticon, log.emotion_color))

    weekday_stats = []
    for i in range(7):
        emotions = weekday_emotions.get(i, [])
        if emotions:
            counter = Counter(emotions)
            (desc, emoticon, color), count = counter.most_common(1)[0]
            weekday_stats.append({
                'weekday': weekday_names[i],
                'emotion': desc,
                'emoticon': emoticon,
                'color': color,
                'count': count
            })
        else:
            weekday_stats.append({
                'weekday': weekday_names[i],
                'emotion': 'Brak danych',
                'emoticon': '',
                'color': '#e5e7eb',
                'count': 0
            })

    return render_template('stats.html'
                           , stats_available=True,
                           most_common_moods=most_common_moods,
                           weekday_stats=weekday_stats)


#EMOTION CREATING IS IMPLEMENTED BUT U CANT USE THEM YET WHILE ADDING LOGS, ITS OPTIONAL PROJECT GOAL SO IT MAY OR NOT BE IMPLEMENTED IN FINAL

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


#WRITTEN LOGS APPEAR IN POPUP FOR NOW AS IT NEEDS ADDICTIONAL FRONTEND DONE, BOX WILL APPEAR IN FINAL PROJECT

@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    form = CalendarLogForm()
    if form.validate_on_submit():
        log_date = form.log_date.data
        log_time = form.log_time.data
        emotions = form.emotions.data
        description = form.description.data
        print(f'Log Date: {log_date}, Log Time: {log_time}, Emotions: {emotions}, Description: {description}')

        new_log = CalendarLog(
            user_id=current_user.id,
            event_date=log_date,
            event_time=log_time,
            description=description,
            emotion_color= emotions.split(',')[0],
            emotion_description=emotions.split(',')[1],
            emotion_emoticon=emotions.split(',')[2] if len(emotions.split(',')) > 2 else None
        )
        db.session.add(new_log)
        db.session.commit()
        flash('Event added successfully!', 'success')

    logs = CalendarLog.query.filter_by(user_id=current_user.id).all()
    logs_dict = []
    logs_by_date = defaultdict(list)
    for log in logs:
        log_dict = {
            'event_date': log.event_date.strftime('%Y-%m-%d'),
            'event_time': log.event_time.strftime('%H:%M') if log.event_time else "",
            'description': log.description,
            'emotion_color': log.emotion_color,
            'emotion_description': log.emotion_description,
            'emotion_emoticon': log.emotion_emoticon
        }
        logs_dict.append(log_dict)
        logs_by_date[log.event_date.strftime('%Y-%m-%d')].append(log_dict)
    return render_template('main.html', form=form, logs=logs_dict, logs_by_date=dict(logs_by_date))

@app.route('/daily')
@login_required
def daily():
    logs = CalendarLog.query.filter_by(user_id=current_user.id).all()
    logs_dict = []
    for log in logs:
        logs_dict.append({
            'event_date': log.event_date.strftime('%Y-%m-%d'),
            'event_time': log.event_time.strftime('%H:%M') if log.event_time else None,
            'description': log.description,
            'emotion_color': log.emotion_color,
            'emotion_description': log.emotion_description,
            'emotion_emoticon': log.emotion_emoticon
        })
    return render_template('daily.html', logs=logs_dict)



## THESE TWO ARE NOT CODED YET (notifs are planned be for final, settings are just simple buttons not important for whole project)

@app.route('/notifs')
@login_required
def notifs():
    return render_template('notifs.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')
