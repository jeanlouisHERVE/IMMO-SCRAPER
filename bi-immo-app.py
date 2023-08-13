#packages
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains

#other modules
from dotenv import load_dotenv

#own packages
import database
database.create_table()

#get data from .env file 
load_dotenv()

#variables
url_immo_website = os.environ["URL_IMMO_WEBSITE_BI"]
driver = webdriver.Chrome()
actions = ActionChains(driver)
chrome_options = ChromeOptions()
city_researched_content = os.environ["CITY_RESEARCHED_CONTENT"]

#functions 
def check_accept_section(cssSelector: str):
    driver.implicitly_wait(5)
    try:
        accept = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, cssSelector)))
        accept.click()
    except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
        print("KO : no accept part")

#script
##connection to website
driver.get(url_immo_website)
driver.implicitly_wait(5)
#check an agree the terms section exists
check_accept_section('span.didomi-continue-without-agreeing')
time.sleep(2)

##fill research section
driver.find_element(By.CSS_SELECTOR, "input.tt-input").send_keys(os.environ["CITY_RESEARCHED"])
time.sleep(2)

#select desired town in the dropdown menu
try:
    dropdown_element = driver.find_elements(By.CSS_SELECTOR, "div.suggestionItem")[0]
    time.sleep(2)
    actions.click(dropdown_element).perform()
except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
    print("KO : unable to make the dropdown menu appear")

#click on the search button
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.search").click()


#catch all the announces
print("------------------Announces Part------------------")
try:
    time.sleep(2)
    articles_ready = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.resultsListContainer")))
    if articles_ready:
        print("test OK")
    articles = driver.find_elements(By.CSS_SELECTOR, "div.sideListItem")
    print("articles",articles)
    for article in articles:
        ###Type of good 
        try:
            type_of_good_content = driver.find_element(By.CSS_SELECTOR,'span.ad-overview-details__ad-title')
            type_of_good_content = type_of_good_content.text
            if "maison" in  type_of_good_content.lower():
                type_of_good = "maison"
            elif "appartement" in type_of_good_content.lower():
                type_of_good = "appartement"
            else:   
                type_of_good = ""
        except (NoSuchElementException):
            print("KO : no element type_of_good")
        print("type_of_good",type_of_good)
        ###town
        town = os.environ["CITY_RESEARCHED_CONTENT"]
        print("town",town)
        ###District&&Postcode
        try:
            address_content = driver.find_element(By.CSS_SELECTOR,'span.ad-overview-details__address-title')
            address_content = address_content.text
            district = re.findall("\((.*?)\)", address_content)[0]
            postcode = re.findall("[0-9]", address_content)[0]
            print("district",district)
        except (NoSuchElementException):
            print("KO : no element type_of_good")
            
        ###Postcode
        
        ###url
except (NoSuchElementException):
    print("KO : no annouces found")
input()

database.connection.close()
driver.close()
driver.quit()
