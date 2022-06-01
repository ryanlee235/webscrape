from flask import Blueprint, render_template, request, flash, url_for,redirect, session
from flask_login import login_required, current_user
from .models import Prices
from. import db
import random 
import os 
views = Blueprint('views',__name__)

@views.route("/")
@views.route("/home", methods=["POST","GET"])
def home():
    if request.method == "POST":
        search = request.form.get('bar')


        return redirect(url_for('views.results'))
    return render_template("home.html")


@views.route('/results')
def results():
    return render_template("results.html")



