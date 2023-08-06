#packages


from selenium import webdriver
from selenium.webdriver.common.by import By
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

#script
driver.get(url_immo_website)
input()

database.connection.close()
driver.close()
driver.quit()
