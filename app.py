from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#from forms import LoginForm, RegisterForm

app = Flask(__name__, static_folder='static', template_folder='templates')

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
