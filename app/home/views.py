from . import home
from flask import render_template,redirect,url_for

@home.route("/")
def index():
    return render_template("/home/index.html")
    #return "<h1 style='color:green'> this is home </h1>"
'''
@home.route("/login/")
def login():
    return render_template("/home/login.html")

@home.route("/logout/")
def logout():
    return redirect(url_for("/home.login"))
'''
