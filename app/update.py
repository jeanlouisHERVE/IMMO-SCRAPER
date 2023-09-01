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

#variable
current_time_utc = datetime.datetime.now(tz=pytz.utc).timestamp()

def update_descriptions():
    for property in database.get_id_url__dateofadding_from_properties():
        id_property, url_property, dateOfAdding_property = property
        timestamp_difference = current_time_utc - dateOfAdding_property
        days_difference = timestamp_difference / (60 * 60 * 24)
        print("days_difference",days_difference)
        
        if int(days_difference) > 7:
            print("url_property", url_property) 
        
        print("property", property)
        ###TODO do not forget to implement an history of the price