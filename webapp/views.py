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
            best_buy()
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
                link_parent = parent_name.find(class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
                if link_parent == None:
                    continue
                link_name = "https://www.amazon.com/"+ link_parent.get("href")
                session['link'] = link_name
                item_name = parent_name.find(class_='a-size-medium a-color-base a-text-normal').text
                session['item-name'] = item_name
                price = parent_name.find(class_='a-price-whole').text
                session['price'] = price
            except:
                pass

        for images in soup.find_all("img"):
            i = images['src']
            session['link-image'] = i

@views.route("/microcenter")
def microcenter():
    if "search" in session:
        search = session['search']
        driver.get('https://www.microcenter.com/')
        nav_Bar = driver.find_element_by_id('search-query')
        nav_Bar.send_keys(search)
        nav_Bar.send_keys(Keys.RETURN)

        search_tab = driver.find_element_by_xpath('//*[@id="pnlMyStoreOnly"]/div/ul/li[2]/a')
        search_tab.click()
        sleep(3)

        r = requests.get(driver.current_url,headers=headers)
        soup = BeautifulSoup(r.content,'html.parser')
        rows = soup.find_all(class_='product_wrapper')
        for i in rows:
                    
            try:
                product_name = i.find(class_="normal").text
                session['microcenter-item'] = product_name
                price = i.find(itemprop="price").text
                session['microcenter-price'] = price
            except:
                pass
            
            link = i.find('a',class_='image')
@views.route('/bestbuy')
def best_buy():
    if "search" in session:
        search = session['search']
    driver.get("https://www.bestbuy.com/")
    search_bar = driver.find_element_by_xpath('//*[@id="gh-search-input"]')
    search_bar.send_keys(search)
    search_bar.send_keys(Keys.RETURN)

    r = requests.get(driver.current_url,headers=headers)
    soup = BeautifulSoup(r.content,"html.parser")

    rows = soup.find(class_='sku-item-list')
    
    for item in rows:

        try:

            information_block = item.find(class_='sku-title').text
            session['best-buy-item-name'] = information_block
            price_block = item.find(class_='priceView-hero-price priceView-customer-price').text.split('$')[-1]
            session['best-buy-price'] = price_block

        except:
            pass


@views.route("/amazon-links")
def amazon_links():
    pass
    
