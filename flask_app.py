from flask import Flask, redirect, url_for, request
from flask import render_template
from Main import main

app = Flask(__name__)

app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        global acct
        acct = request.form['contents']
        main(acct)
        return redirect(url_for('map'))


@app.route("/map", methods=["GET"])
def map():
    return render_template("{0}.html".format(acct))


if __name__ == '__main__':
    app.run()