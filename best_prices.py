import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import re

search_term = input('enter product: ')
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

amazon_products = []
microcenter_products = []


def amazon():
    driver.get('https://www.amazon.com/')
    driver.implicitly_wait(10)
    nav_bar = driver.find_element_by_id('twotabsearchtextbox')
    nav_bar.send_keys(search_term)
    nav_bar.send_keys(Keys.RETURN)
    
    r = requests.get(driver.current_url,headers=headers)
    print(r)
    soup = BeautifulSoup(r.content, 'lxml')
    sections = soup.find_all(class_='a-section')
    
    for item in sections:
        
        
        parent = item.parent

        if parent.name != 'a':
            continue

        link = parent['href']
        
        parent_name = item.find_parent(class_='sg-row')
            
        try:
            item_name = parent_name.find(class_='a-size-medium a-color-base a-text-normal').text
            amazon_products.append(item_name)
            price = parent_name.find(class_='a-price-whole').text
            price.join("price:")
            amazon_products.append(price)
            
        except:
            pass

       
def microcenter():
    driver.get('https://www.microcenter.com/')
    nav_Bar = driver.find_element_by_id('search-query')
    nav_Bar.send_keys(search_term)
    nav_Bar.send_keys(Keys.RETURN)

    search_tab = driver.find_element_by_xpath('//*[@id="pnlMyStoreOnly"]/div/ul/li[2]/a')
    search_tab.click()
    sleep(3)
    r = requests.get(driver.current_url,headers=headers)
    soup = BeautifulSoup(r.content,'html.parser')
    rows = soup.find_all(class_='product_wrapper')
    for i in rows:
        

        product_name = i.find(class_="normal").text
        microcenter_products.append(product_name)
        product_name.join("item:")
        try:

            price = i.find(itemprop="price").text
            price.join("price:")
            microcenter_products.append(price)
        except:
            pass
        
        link = i.find('a',class_='image')
        microcenter_products.append("https://www.microcenter.com" + link.get('href'))


def items():
    amazon_product_new = [i for n, i in enumerate(amazon_products) if i not in amazon_products[:n]]
    print("AMAZON")
    print("-----------------")
    for i in amazon_product_new:
        print(i, sep="", end="\n")
    print("---------------------")
    print("MICROCENTER")
    for i in microcenter_products[:9]:
        print(i)

        
     
if __name__ == '__main__':
    amazon()
    microcenter()
    items()