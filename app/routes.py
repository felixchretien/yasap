from flask import render_template
from app import app
import lorem


@app.route('/')
def index():
    return render_template("home.html", title='Home', active="home", message=lorem.text())
