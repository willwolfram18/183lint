from flask import Flask, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True


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
    print request.files.getlist('files[]')
    return 'Server received data'



if __name__ == '__main__':
    app.run(debug=True)