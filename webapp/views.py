from flask import Blueprint, render_template, request, flash, url_for,redirect, session
from flask_login import login_required, current_user
from .models import Prices
from. import db
import random 
import os 
views = Blueprint('views',__name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("base.html")



