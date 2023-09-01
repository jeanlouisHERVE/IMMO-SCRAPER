#packages
import os
import re
import time
import pytz
import datetime
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
import functions

#get data from .env file 
load_dotenv()

#variables
driver = webdriver.Chrome()
actions = ActionChains(driver)
chrome_options = ChromeOptions()
url_immo_website = os.environ["URL_IMMO_WEBSITE_BI"]
city_researched_content = os.environ["CITY_RESEARCHED_CONTENT"]
current_time_utc = datetime.datetime.now(tz=pytz.utc).timestamp()

def update_descriptions():
    for property in database.get_id_url_dateofmodification_from_properties():
        id_property, url_property, dateOfModification_announce = property
        # timestamp_difference = current_time_utc - dateOfModification_announce
        # days_difference = timestamp_difference / (60 * 60 * 24)
        # print("days_difference",days_difference)
        
        # if int(days_difference) > 7:
        #     print("url_property", url_property) 
        ###TODO check if the date of modification is different from the one registered
        ###TODO do not forget to implement an history of the price