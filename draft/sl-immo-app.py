# packages
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains

# other modules
from dotenv import load_dotenv

# own packages
#import database
# database.create_table()

#get data from .env file 
load_dotenv()

# variables
url_immo_website= os.environ["URL_IMMO_WEBSITE"]
driver = webdriver.Chrome()
actions = ActionChains(driver)
chrome_options = ChromeOptions()
city_researched_content = os.environ["CITY_RESEARCHED_CONTENT"]


# functions 
def check_accept_section(cssSelector: str):
    driver.implicitly_wait(5)
    try:
        accept = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, cssSelector)))
        accept.click()
    except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
        print("KO : no accept part")

# script
## connection to website
driver.get(url_immo_website)
driver.implicitly_wait(5)
check_accept_section('span.didomi-continue-without-agreeing')
time.sleep(2)

## fill research section
# remove pre selected area "Ile de France"
driver.find_element(By.CSS_SELECTOR, "div.sc-gLDzan.bevJHu").click()
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "input.sc-irTswW.fPqHAw").send_keys(os.environ["CITY_RESEARCHED"])
time.sleep(2)

# elect desired town in the dropdown menu => to fix
try:
    dropdown_element = driver.find_element(By.CSS_SELECTOR, "div.sc-ktEKTO.kSmfsP input.sc-irTswW.fPqHAw")
    time.sleep(2)
    actions.click(dropdown_element).perform()
except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
    print("KO : unable to make the dropdown menu appear")
    
# select desired option in the dropdown menu => to fix 
xpath_expression = '//span[@data-testid="gsl.uilib.Droplist.Option.1"]'   
try:
    town_option = driver.find_element(By.XPATH, '//div[@data-testid="gsl.uilib.Droplist.Option.1"]')
    time.sleep(2)
    actions.click(town_option).perform()
except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
    print("KO : unable to select the option in the dropdown menu")

# click on the search button
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "button.sc-bZPPFW.gurgxX").click()
input()

#database.connection.close()
driver.close()
driver.quit()
