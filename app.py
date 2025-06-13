from flask import Flask, render_template

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def hello_world():
 return 'Hello, World!'

@app.route('/start')
def start():
 return render_template('start.html')

@app.route('/login')
def login():
 return render_template('login.html')