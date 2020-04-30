from flask import Flask, render_template, request, session
from flask_session import Session
from random import shuffle

app = Flask(__name__)
app.secret_key = 'super secret key'

app.config['SESSION_PERMANENT'] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/', methods=['GET'])
def index():
    if session.get('name') is None:
        session['bucket'] = []
        return render_template("login.html")
    else:
        return render_template("index.html", bucket=session['bucket'], name=session['name'])


@app.route('/', methods=['POST'])
def login():
    session['name'] = request.form.get('name')
    return render_template("index.html", bucket=session['bucket'], name=session['name'])


@app.route('/add_item', methods=['POST'])
def add_item():
    item = request.form.get('new_item')
    if len(item) != 0:
        session['bucket'].append(item)
    print(session['bucket'])
    return render_template("index.html", bucket=session['bucket'], name=session['name'])


@app.route('/remove_item', methods=['POST'])
def remove_item():
    item = request.form.get('item-to-remove')
    if item in session['bucket']:
        session['bucket'].remove(item)
        return render_template("index.html", bucket=session['bucket'], name=session['name'])
    return "You tried removing something that doesn't exist!"


@app.route('/shuffle', methods=['POST', 'GET'])
def shuffle_bucket():
    shuffle(session['bucket'])
    return render_template("index.html", bucket=session['bucket'], name=session['name'])


@app.route('/clear', methods=['GET', 'POST'])
def clear():
    if session.get('bucket') is not None:
        session['bucket'].clear()
        return render_template("index.html", bucket=session['bucket'], name=session['name'])


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['name'] = None
    return render_template("login.html")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def oops(path):
    return render_template('error.html', path=path)


if __name__ == '__main__':
    app.run(debug=True)