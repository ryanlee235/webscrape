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
options.add_argument('--no-proxy-server')
options.add_argument("--proxy-server='direct://'")
options.add_argument("proxy-bypass-list=*")
options.add_argument('--blink-setting=imagesEnabled=flase')
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
amazon_link = []

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
            microcenter()
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
        name = soup.find(class_='a-size-medium a-color-base a-text-normal').text[:70]
        session['item-name'] = name
        price = soup.find(class_="a-price-whole").text
        session['price'] = price
        link = soup.find(class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
        link_name = "https://www.amazon.com/" + link.get('href') 
        session['link'] = link_name

      

@views.route("/microcenter")
def microcenter():
    if "search" in session:
        search = session['search']
        driver.get('https://www.microcenter.com/')
        nav_Bar = driver.find_element_by_id('search-query')
        nav_Bar.send_keys(search)
        nav_Bar.send_keys(Keys.RETURN)
        sleep(3)
        search_tab = driver.find_element_by_xpath('//*[@id="pnlMyStoreOnly"]/div/ul/li[2]/a')
        search_tab.click()
        sleep(3)

        r = requests.get(driver.current_url,headers=headers)
        soup = BeautifulSoup(r.content,'html.parser')
    

        link_parent = soup.find('a',class_='image')
        link_name = link_parent.get("href")
        link = "https://www.microcenter.com" + link_name
        session['link-microcenter'] = link
        product_name = soup.find(class_="normal").text[:70]
        session['microcenter-item'] = product_name
        price = soup.find(itemprop="price").text
        session['microcenter-price'] = price
        
            
