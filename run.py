from functools import wraps
from flask import Flask, render_template, request, redirect, session, url_for
from flask_googlelogin import GoogleLogin
from os import mkdir
import os.path
from werkzeug import secure_filename

app = Flask(__name__)

app.config['SECRET_KEY'] = ''
app.config['GOOGLE_LOGIN_CLIENT_ID'] = ''
app.config['GOOGLE_LOGIN_CLIENT_SECRET'] = ''
app.config['GOOGLE_LOGIN_REDIRECT_URI'] = 'http://localhost:5000/oauth2callback'
google = GoogleLogin(app)

app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = 'uploads'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['USERNAME'] is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function



@app.route('/')
@app.route('/index')
def index():
    if 'USERNAME' not in session:
        session['USERNAME'] = None
    return render_template('index.html', username=session['USERNAME'], current='index')

@app.route('/about')
def about():
    if 'USERNAME' not in session:
        session['USERNAME'] = None
    return render_template('about.html', username=session['USERNAME'], current='about')

@app.route('/contact')
def contact():
    if 'USERNAME' not in session:
        session['USERNAME'] = None
    return render_template('contact.html', username=session['USERNAME'], current='contact')

@app.route('/contribute')
def contribute():
    if 'USERNAME' not in session:
        session['USERNAME'] = None
    return render_template('contribute.html', username=session['USERNAME'], current='contribute')

@app.route('/upload_files', methods=['POST'])
@login_required
def gradeFiles():
    receivedFiles = request.files.getlist('files[]')
    savedFiles = []
    for f in receivedFiles:
        filename = secure_filename(f.filename)
        if filename != '':
            pathname = '/'.join([app.config['UPLOAD_FOLDER'], session['USER_ID']])
            if not os.path.exists(os.path.join(pathname)):
                mkdir(pathname)
            f.save(os.path.join(pathname, filename))
            savedFiles.append(filename)
    print 'The following files were saved: {}'.format(savedFiles)
    return 'Success'


# Functions for Logging in and out using Google
@app.route('/login', methods=['GET'])
def login():
    if 'USERNAME' not in session:
        session['USERNAME'] = None
    return redirect(google.login_url(prompt="select_account", params=dict(next=request.args.get('next'))))

@app.route('/logout')
def logout():
    session['USERNAME'] = None
    return redirect(url_for('index'))

@app.route('/oauth2callback')
@google.oauth2callback
def callback(token, userinfo, **params):
    session['USERNAME'] = userinfo['name']
    session['USER_ID'] = userinfo['id']
    session['TOKEN'] = token
    return redirect(url_for(params['next']))

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])