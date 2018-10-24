from flask import Flask, jsonify, render_template, request, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'super secret key'

app.config['SESSION_PERMANENT'] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods=['GET'])
def index():
    if session.get('bucket') is None:
        session['bucket'] = []
    return render_template("index.html", bucket=session['bucket'])


@app.route('/add_item', methods=['POST'])
def add_item():
    item = request.form.get('new_item')
    if len(item) is not 0:
        session['bucket'].append(item)
    print(session['bucket'])
    return render_template("index.html", bucket=session['bucket'])


@app.route('/clear', methods=['GET', 'POST'])
def clear():
    if session.get('bucket') is not None:
        session['bucket'][:] = []
    return render_template("index.html", bucket=session['bucket'])


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def oops(path):
    return render_template('error.html', path=path)