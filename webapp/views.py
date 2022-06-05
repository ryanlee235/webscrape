from flask import Blueprint, render_template, request, flash, url_for,redirect, session
from flask_login import login_required, current_user
import os 
import requests
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import re
PATH ="C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--log-level=5")
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')
driver = webdriver.Chrome(PATH,options=options)

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)',
    'cache-control': 'no-cache',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-langauge': 'en-US,en;q=0.9'

}




views = Blueprint('views',__name__)

@views.route('/', methods=['POST','GET'])
def home():
    if request.method == "POST":
        search = request.form.get("bar")
        session['search'] = search
        if len(search) < 1:
            flash("Please enter product you are looking for!", category='error')

        else:
            amazon()
            return redirect(url_for('views.results'))

    return render_template("home.html")


@views.route('/results', methods=["GET", "POST"])
def results():
    return render_template("result.html")
    


@views.route('/amazon')
def amazon():
    if 'search' in session:
        search = session['search']
        
        driver.get('https://www.amazon.com/')
        nav_bar = driver.find_element_by_id("twotabsearchtextbox")
        nav_bar.send_keys(search)
        nav_bar.send_keys(Keys.RETURN)

        r = requests.get(driver.current_url,headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        sections = soup.find_all(class_='a-section')

        for item in sections:
            parent = item.parent

            parent_name = item.find_parent(class_='sg-row')

            try:
                sponsored = parent_name.find(class_='s-label-popover-default')
                if sponsored:
                    pass
                elif not sponsored:
                    item_name = parent_name.find(class_='a-size-medium a-color-base a-text-normal').text
                    session['item-name'] = item_name
                    price = parent_name.find(class_='a-price-whole').text
                    session['price'] = price
            except:
                pass

        for images in soup.find_all("img"):
            i = images['src']
            session['link-image'] = i

