from email import header
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import re
search_term = input("enter something: ")
PATH ="C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--log-level=5")
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')
driver = webdriver.Chrome(PATH)

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
    soup = BeautifulSoup(r.content, 'html.parser')
    section = soup.find_all(class_="a-section")

    for i in section:
        try:
            name = i.find(class_='a-size-medium a-color-base a-text-normal').text
            price = i.find(class_="a-price-whole").text
            link = i.find(class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
        except:
            pass
 
    return name, price
     

    #price = driver.find_element_by_css_selector(".widgetId\=search-results_1 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > span:nth-child(1) > span:nth-child(2) > span:nth-child(2)").text
    #link = driver.find_element_by_partial_link_text("/").text
    
    #print(price)
    #print(link)
       
def microcenter():
    driver.get('https://www.microcenter.com/')
    nav_Bar = driver.find_element_by_id('search-query')
    nav_Bar.send_keys(search_term)
    nav_Bar.send_keys(Keys.RETURN)
    sleep(3)
    search_tab = driver.find_element_by_xpath('//*[@id="pnlMyStoreOnly"]/div/ul/li[2]/a')
    search_tab.click()
    sleep(3)
    r = requests.get(driver.current_url,headers=headers)
    soup = BeautifulSoup(r.content,'html.parser')
    product_name = soup.find(class_="normal").text   
    price = soup.find(itemprop="price").text
    link_class = soup.find('a',class_='image')
    link = link_class.get("href")
    print(product_name)
    print(price)
    print(link)
    


def best_buy():

    url = 'https://www.bestbuy.com/site/searchpage.jsp?st={search_term}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,"html.parser")
    


    

      
    information_block = soup.find(class_='sku-title').text
    
    # price_block = soup.find(class_='priceView-hero-price priceView-customer-price').text.split('$')[-1]
          

        

def new_egg():
    driver.get("https://www.newegg.com/")
    search_bar = driver.find_element_by_css_selector('.header2021-search-box > input:nth-child(1)')
    search_bar.send_keys(search_term)
    search_bar.send_keys(Keys.RETURN)
    sleep(5)

    item_click = driver.find_element_by_class_name("item-img")
    item_click.click()
    #name = driver.find_element_by_class_name('product-title').text

    
    
    
    







# def items():
#     amazon_product_new = [i for n, i in enumerate(amazon_products) if i not in amazon_products[:n]]
#     print("AMAZON")
#     print("-----------------")
#     for i in amazon_product_new:
#         print(i, sep="", end="\n")
#     print("---------------------")
#     print("MICROCENTER")
    
#     print(microcenter_products[:9])

        
     
if __name__ == '__main__':
    new_egg()
#     items()

# def best_buy():
#     if "search" in session:
#         search = session['search']
#     driver.get("https://www.bestbuy.com/")
#     search_bar = driver.find_element_by_xpath('//*[@id="gh-search-input"]')
#     search_bar.send_keys(search)
#     search_bar.send_keys(Keys.RETURN)

#     r = requests.get(driver.current_url,headers=headers)
#     soup = BeautifulSoup(r.content,"html.parser")

#     rows = soup.find(class_='sku-item-list')
    
#     for item in rows:

#         try:

#             information_block = item.find(class_='sku-title').text
#             session['best-buy-item-name'] = information_block
#             price_block = item.find(class_='priceView-hero-price priceView-customer-price').text.split('$')[-1]
#             session['best-buy-price'] = price_block

#         except:
#             pass