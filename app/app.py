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
database.create_table()
import update
import add_announces

#get data from .env file 
load_dotenv()

#variables
city_researched_content = os.environ["CITY_RESEARCHED_CONTENT"]
menu_prompt = """-- Menu --

1) Refresh database
2) Run script to add description
3) Update descriptions
4) Number of announces
5) Exit

Enter your choice: """



###TODO update announces
###TODO send old announces to another table

def start_prompt(): 
    while (user_input := input(menu_prompt)) != "5":
        if user_input == "1":
            add_announces.add_new_announces()
        elif user_input == "2":
            add_announces.add_descriptions()
        elif user_input == "3":
            update.update_descriptions()
        elif user_input == "4":
            global_properties_number = database.get_properties_number()
            print(f"""\n--- The properties number --- \n\n The city {city_researched_content} has a total of {global_properties_number[0][0]} properties to sell. \n 
                  """)
        else:
            print("Invalid input, please try again!")

#script
start_prompt()