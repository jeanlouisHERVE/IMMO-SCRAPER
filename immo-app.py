#packages
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions

#other modules
from dotenv import load_dotenv

#own packages
import database
database.create_table()

#get data from .env file 
load_dotenv()

#variables
city_researched="Sar"
url_immo_website="https://www.seloger.com/vente.htm"
driver = webdriver.Chrome()
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
check_accept_section('span.didomi-continue-without-agreeing')
driver.implicitly_wait(5)

##fill research section
#remove pre selected area "Ile de France"
driver.find_element(By.CSS_SELECTOR, "div.sc-gLDzan.bevJHu").click()
driver.find_element(By.CSS_SELECTOR, "input.sc-irTswW.fPqHAw").send_keys(os.environ["CITY_RESEARCHED"])
driver.implicitly_wait(5)
#select desired town in the dropdown menu => to fix 
xpath_expression = '//span[@value="' + city_researched_content + '"]'
driver.find_element(By.XPATH, xpath_expression).click()
#driver.find_element(By.CSS_SELECTOR, "button.sc-bZPPFW.gurgxX").click()

input()

database.connection.close()
driver.close()
driver.quit()
