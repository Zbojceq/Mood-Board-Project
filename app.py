from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegisterForm
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__, static_folder='static', template_folder='templates')

app.config['SECRET_KEY'] = '123456789' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager() #implementuje moduł logowania 
login_manager.init_app(app)
login_manager.login_view = 'login_temp'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Czas trwania sesji
csrf = CSRFProtect(app)  # Inicjalizacja CSRF Protect


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@app.route('/login_temp', methods=['GET', 'POST'])
def login_temp():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login_temp.html', form=form)

@app.route('/register_temp', methods=['GET', 'POST'])
def register_temp():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login_temp'))
    return render_template('register_temp.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_temp'))

@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}!'


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/register')
def register():
    return render_template('register.html') 

@app.route('/login')
def login():
    return render_template('login.html') 

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
def stats():
    return render_template('stats.html')

@app.route('/emotion_create')
def emotion_create():
    return render_template('emotion_create.html')

@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/side_menu')
def side_menu():
    return render_template('side_menu.html')

@app.route('/notifs')
def notifs():
    return render_template('notifs.html')

@app.route('/emotion_add')
def emotion_add():
    return render_template('emotion_add.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')
