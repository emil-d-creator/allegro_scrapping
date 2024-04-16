import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-logging"])

#CHANGE PATH HERE ALSO
options.binary_location = "F:\webdrive\chrome-win64\chrome-win64\\chrome.exe"
PATH = r'F:\webdrive\chromedriver.exe' 
service = webdriver.chrome.service.Service(PATH)
driver = webdriver.Chrome(service=service, options=options)
search=input("Type text to search : ")

search.replace(" ","%20")
driver.get(fr'https://allegrolokalnie.pl/oferty/q/{search}')
time.sleep(2)
b = driver.find_element(By.CSS_SELECTOR, '[data-testid="accept_home_view_action"]')
b.click()
time.sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
strony = driver.find_element(By.CLASS_NAME, "ml-pagination__input")
s = int(strony.get_attribute("max"))
print("Number of pages scraped  : ", s)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

all_data = []

for i in range(0,s+1):   
    time.sleep(2)

    ad = driver.find_elements(By.CSS_SELECTOR, '[itemprop="itemOffered"]')
    ce = driver.find_elements(By.CLASS_NAME, "ml-offer-price__dollars")
    wal = driver.find_elements(By.CLASS_NAME, "ml-offer-price__currency")
    addr = driver.find_elements(By.CSS_SELECTOR, '[itemprop="address"]')
    link = driver.find_elements(By.CSS_SELECTOR, '[itemprop="url"]')[1:]

    for a, c, w, ad, l in zip(ad, ce, wal, addr, link):
        all_data.append((l.get_attribute("href"), a.text, c.text, w.text, ad.text))

    time.sleep(2)
    
    
    if s!=1:
        page_input = driver.find_elements(By.CLASS_NAME, "ml-pagination__input")    
        page_input[1].clear()
        page_input[1].send_keys(i+1)
        page_input[1].send_keys(Keys.ENTER)




df = pd.DataFrame(all_data, columns=["Link", "Name", "Price", "Currency", "Address"])


try:
    #change path here
    df.to_excel(fr'F:\pobrane nowe\pythek\webscraping uporządkowany\PROJEKT 9 ALLEGRO\excell\allegrolokalnie-{search}.xlsx', index=False)
    print("DATA SAVED ")
except Exception as e:
    print("ERROR :")
    print(e)

driver.quit()
