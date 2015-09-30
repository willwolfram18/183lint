from ConfigParser import ConfigParser
from functools import wraps
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask.ext.assets import Environment, Bundle
from flask_googlelogin import GoogleLogin
from os import mkdir
import os.path
from StyleGrader import StyleRubric
from werkzeug import secure_filename

config = ConfigParser()
config.read('/var/www/183lint/183lint/config.ini')

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = config.get('SETTINGS', 'upload_location')

app.config['SECRET_KEY'] = ''

# Google Info for Google Login
app.config['GOOGLE_LOGIN_CLIENT_ID'] = ''
app.config['GOOGLE_LOGIN_CLIENT_SECRET'] = ''
app.config['GOOGLE_LOGIN_REDIRECT_URI'] = 'http://style183.eecs.umich.edu/oauth2callback'
                                                                                
google = GoogleLogin(app)
assets = Environment(app)
assets.url = app.static_url_path
sass = Bundle('presentation/styles.scss', filters="pyscss", output="presentation/styles.css")
assets.register('scss_all', sass)

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
    # Data to display on the about page
    styleGuideURL = "https://eecs183.org/docs/style/"
    panels = [
        {
            'id': 'panel-0',
            'title': 'Why was 183lint built?',
            'description': '183lint is a program designed for the EECS 183 course at the University of Michigan.' +
                           ' It was created as a way to give students the ability to check some aspects of their C++ code quality.',
        },
        {
            'id': 'panel-1',
            'title': 'How does 183lint work?',
            'description': '183lint is built using Python\'s Flask library, and uses Python\'s bindings to Clang in order' +
                           ' to parse the submitted code.  For information on the Clang bindings, feel free to read ' +
                           '<a href="http://eli.thegreenplace.net/2011/07/03/parsing-c-in-python-with-clang">this article</a>.',
        },
        {
            'id': 'panel-2',
            'title': 'What does 183lint check?',
            'description': '183lint is capable of checking the following aspects of C++ code, according to the standards in the ' +
                           '<a target="_blank" href="{}">EECS 183 Style Guidelines</a>.'.format(styleGuideURL),
            'bullets': [
                'Correct operator spacing',
                'Use of the ternary operator',
                'Improper use of a <tt>break</tt> statement',
                'Improper use of a <tt>continue</tt> statement',
                'Any use of a <tt>goto</tt> statement',
                'Continuous loops using <tt>while(true)</tt> or <tt>while(!false)</tt>',
                'Comparison to boolean literals such as <tt>x == true</tt>',
                'Each line does not exceed the suggested {} character limit'.format(config.get('SETTINGS', 'line_length')),
                'Files do not include any excluded libraries'
            ],
        },
    ]
    return render_template('about.html', username=session['USERNAME'], current='about', panels=panels)

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
            pathname = os.path.join(app.config['UPLOAD_FOLDER'], session['USER_ID'])
            if not os.path.exists(pathname):
                mkdir(pathname)
            filename = os.path.join(pathname, filename)
            f.save(filename)
            savedFiles.append(filename)
            
    rubric = StyleRubric(optionalConfig=config)
    for f in savedFiles:
        rubric.gradeFile(f)

    finalReport = rubric.generateReport()
    return jsonify(finalReport)


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
