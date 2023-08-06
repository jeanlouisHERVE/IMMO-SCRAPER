#packages


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions

#own packages
import database
database.create_table()


#variables
url_immo_website="https://www.seloger.com/vente.htm"
driver = webdriver.Chrome()
chrome_options = ChromeOptions()

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

input()

database.connection.close()
driver.close()
driver.quit()
