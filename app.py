from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegisterForm, EmotionForm, CalendarLogForm, NotificationForm
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from collections import Counter, defaultdict
from flask_mail import Mail, Message
from sqlalchemy.types import PickleType
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


app = Flask(__name__, static_folder='static', template_folder='templates')

app.config['SECRET_KEY'] = '123456789' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager() 
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  
csrf = CSRFProtect(app)  


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'moodboardwebapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'sqlpqjjnqdwxskiv' 

mail = Mail(app)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    calendar_logs = db.relationship('CalendarLog', backref='user', lazy=True, cascade='all, delete-orphan')
    emotions = db.relationship('Emotion', backref='user', lazy=True, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade='all, delete-orphan')

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

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notification_times = db.Column(PickleType, nullable=False, default=lambda: [None, None, None, None])
    notification_enabled = db.Column(PickleType, nullable=False, default=lambda: [False, False, False, False])

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
    for i in range(len(current_user.notifications)):
        print(f'Notification {i}: Times: {current_user.notifications[i].notification_times}, Enabled: {current_user.notifications[i].notification_enabled}')
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
        return redirect(url_for('main'))
    return render_template('emotion_create.html', form=form)



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
        
    logs = CalendarLog.query.filter_by(user_id=current_user.id).all()
    logs_dict = []
    logs_by_date = defaultdict(list)
    for log in logs:
        log_dict = {
            'id': log.id,
            'event_date': log.event_date.strftime('%Y-%m-%d'),
            'event_time': log.event_time.strftime('%H:%M') if log.event_time else "",
            'description': log.description,
            'emotion_color': log.emotion_color,
            'emotion_description': log.emotion_description,
            'emotion_emoticon': log.emotion_emoticon
        }
        logs_dict.append(log_dict)
        logs_by_date[log.event_date.strftime('%Y-%m-%d')].append(log_dict)
    now = datetime.now()
    return render_template('main.html', form=form, logs=logs_dict, logs_by_date=dict(logs_by_date),now=now)

@app.route('/daily')
@login_required
def daily():
    logs = CalendarLog.query.filter_by(user_id=current_user.id).all()
    logs_dict = []
    for log in logs:
        logs_dict.append({
            'id': log.id,
            'event_date': log.event_date.strftime('%Y-%m-%d'),
            'event_time': log.event_time.strftime('%H:%M') if log.event_time else None,
            'description': log.description,
            'emotion_color': log.emotion_color,
            'emotion_description': log.emotion_description,
            'emotion_emoticon': log.emotion_emoticon
        })
    return render_template('daily.html', logs=logs_dict)

@app.route('/delete_log', methods=['POST'])
@login_required
@csrf.exempt
def delete_log():
    data = request.get_json()
    log_id = data.get('id')
    if not log_id:
        return jsonify({'success': False, 'error': 'No log id provided'}), 400
    log = CalendarLog.query.filter_by(id=log_id, user_id=current_user.id).first()
    if log:
        db.session.delete(log)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Log not found'}), 404


@app.route('/notifs', methods=['GET', 'POST'])
@login_required
def notifs():
    form = NotificationForm()
    notification = Notification.query.filter_by(user_id=current_user.id).first()
    if not notification:
        notification = Notification(user_id=current_user.id, notification_times=[None, None, None, None], notification_enabled=[False, False, False, False])
        db.session.add(notification)
        db.session.commit()
    print(f'Notification: {notification}')
    if request.method == 'POST':
        notification.notification_times = [
            form.notification_time_morning.data,
            form.notification_time_afternoon.data,
            form.notification_time_evening.data,
            form.notification_time_night.data
        ]
        notification.notification_enabled = [
            bool(form.notification_enabled_morning.data),
            bool(form.notification_enabled_afternoon.data),
            bool(form.notification_enabled_evening.data),
            bool(form.notification_enabled_night.data)
        ]
        db.session.commit()
        print('Notification settings updated!', 'success')
        schedule_user_notifications(scheduler)
        return redirect(url_for('notifs'))
    return render_template('notifs.html', form=form)


@app.route('/get_notif_data', methods=['POST'])
@login_required
def get_notif_data():
    notification = Notification.query.filter_by(user_id=current_user.id).first()
    if notification:
        times = [t.strftime('%H:%M') if t else None for t in notification.notification_times]
        return jsonify({
            'notification_times': times,
            'notification_enabled': notification.notification_enabled
        })
    return jsonify({'error': 'No notification settings found.'}), 404







@app.route('/settings', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@login_required
def settings():
    if request.method == 'GET':
        return render_template('settings.html')
    if request.method == 'POST':
        return jsonify({
            'username': current_user.username,
            'email': current_user.email
        })
    if request.method == 'PATCH':
        data = request.get_json()
        action = data.get('action')
        if action == 'change_username':
            password = data.get('password')
            new_username = data.get('new_username')
            if not check_password_hash(current_user.password, password):
                return jsonify({'success': False, 'error': 'Incorrect password.'})
            if not new_username or len(new_username) < 3:
                return jsonify({'success': False, 'error': 'Username too short.'})
            if User.query.filter_by(username=new_username).first():
                return jsonify({'success': False, 'error': 'Username already taken.'})
            current_user.username = new_username
            db.session.commit()
            return jsonify({'success': True})
        elif action == 'change_email':
            password = data.get('password')
            new_email = data.get('new_email')
            if not check_password_hash(current_user.password, password):
                return jsonify({'success': False, 'error': 'Incorrect password.'})
            if not new_email or '@' not in new_email:
                return jsonify({'success': False, 'error': 'Invalid email.'})
            if User.query.filter_by(email=new_email).first():
                return jsonify({'success': False, 'error': 'Email already in use.'})
            current_user.email = new_email
            db.session.commit()
            return jsonify({'success': True})
        elif action == 'change_password':
            old_password = data.get('old_password')
            new_password1 = data.get('new_password1')
            new_password2 = data.get('new_password2')
            if not check_password_hash(current_user.password, old_password):
                return jsonify({'success': False, 'error': 'Incorrect current password.'})
            if not new_password1 or len(new_password1) < 4:
                return jsonify({'success': False, 'error': 'Password too short.'})
            if new_password1 != new_password2:
                return jsonify({'success': False, 'error': 'Passwords do not match.'})
            current_user.password = generate_password_hash(new_password1, method='pbkdf2')
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Invalid action.'})
    if request.method == 'DELETE':
        data = request.get_json(silent=True) or {}
        password = data.get('password')
        if not password or not check_password_hash(current_user.password, password):
            return jsonify({'success': False, 'error': 'Incorrect password.'})
        user = User.query.get(current_user.id)
        user_id = user.id  # Save id before logout
        logout_user() 
        # Remove user after logout (session is now anonymous)
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'success': True, 'redirect': url_for('login')})
        else:
            return jsonify({'success': False, 'error': 'User not found.'})




def send_notification_to_user(user, notif_type):
    with app.app_context():
        msg = Message(
            subject="Your Daily Mood Board Reminder",
            sender=app.config['MAIL_USERNAME'],
            recipients=[user.email],
            body=f"Don't forget to log your {notif_type} mood today!"
        )
        mail.send(msg)

def schedule_user_notifications(scheduler):
    with app.app_context():
        users = User.query.all()
        for user in users:
            notification = Notification.query.filter_by(user_id=user.id).first()
            if notification:
                times = notification.notification_times
                enabled = notification.notification_enabled
                labels = ['Morning', 'Afternoon', 'Evening', 'Night']
                for i in range(4):
                    if enabled[i] and times[i]:
                        hour = times[i].hour
                        minute = times[i].minute
                        job_id = f"notif_{user.id}_{i}"
                        scheduler.remove_job(job_id=job_id, jobstore=None) if job_id in [j.id for j in scheduler.get_jobs()] else None
                        scheduler.add_job(
                            send_notification_to_user,
                            trigger=CronTrigger(hour=hour, minute=minute),
                            args=[user, labels[i]],
                            id=job_id,
                            replace_existing=True
                        )

scheduler = BackgroundScheduler()
schedule_user_notifications(scheduler)
scheduler.start()
