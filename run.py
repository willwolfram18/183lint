from flask import Flask, render_template, request
import os.path
from werkzeug import secure_filename

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = 'uploads/'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/contribute')
def contribute():
    return render_template('contribute.html')

@app.route('/upload_files', methods=['POST'])
def gradeFiles():
    receivedFiles = request.files.getlist('files[]')
    savedFiles = []
    for f in receivedFiles:
        filename = secure_filename(f.filename)
        if filename != '':
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            savedFiles.append(filename)
    print 'The following files were saved: {}'.format(savedFiles)
    return 'Success'



if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])