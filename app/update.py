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

#functions 
def check_accept_section(cssSelector: str):
    driver.implicitly_wait(5)
    try:
        accept = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, cssSelector)))
        accept.click()
    except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
        print("KO : no accept part")

def update_descriptions():
    for property in database.get_id_url_dateofmodification_from_properties():
        id_property, url_property, dateOfModification_announce = property
        
        print("step1")
        driver.get(url_property)
        driver.implicitly_wait(5)

        check_accept_section('span.didomi-continue-without-agreeing')
        driver.implicitly_wait(5)

        print("step2")
        
        labelsInfo = driver.find_elements(By.CSS_SELECTOR, "div.labelInfo")
        
        ###default values
        ##building options
        new_year_of_construction = ""
        new_exposition = ""
        new_floor = None
        new_total_floor_number = None
        new_neighborhood_description = ""

        ##rooms
        new_bedroom_number = 0
        new_toilet_number = 0
        new_bathroom_number = 0
        new_cellar = False
        new_lock_up_garage = False

        ##options indoor
        new_heating = ""
        new_tv_cable = False
        new_fireplace = False
        new_digicode = False
        new_intercom = False
        new_elevator = False
        new_fibre_optics_status = ""

        #options outdoor
        new_garden = False
        new_car_park_number = 0
        new_balcony = False
        new_large_balcony = False

        ##administration
        new_estate_agency_fee_percentage = 0
        new_pinel = False
        new_denormandie = False
        new_announce_publication = ""
        new_announce_last_modification = ""
        
        ##diagnostics
        new_dpe_date = ""
        new_energetic_performance_letter = None
        new_energetic_performance_number = 0 
        new_climatic_performance_number = 0
        new_climatic_performance_letter = None
        
        
        regex_find_numbers = r'\d+'
        regex_find_text_after_colon = r':\s*([^:,]+)'
        
        print("step3")
        for labelInfo in labelsInfo:
            
            try:
                element = labelInfo.find_element(By.CSS_SELECTOR, "span")
                element_text = element.text.lower()
                print('element_text ',element_text )
                
                # year_of_construction
                if "construit" in element_text:
                    new_year_of_construction = re.findall(regex_find_numbers, element_text)[0]
                    format_string_construction = "%Y"
                    local_timestamp_construction = datetime.datetime.strptime(year_of_construction, format_string_construction)
                    new_year_of_construction = local_timestamp_construction.replace(tzinfo=pytz.timezone('UTC')).timestamp()
                
                #exposition
                elif "exposé" in element_text:
                    pattern_exposition = r'exposé\s(.+)'
                    new_exposition = re.findall(pattern_exposition, element_text)[0]
                
                #floor
                #total_floor_number 
                elif "étage" in element_text:
                    pattern_floor = r'^[0-9]+'
                    pattern_floor_number = r'sur\s+(\d+)'
                    
                    if "dernier" in element_text:
                        new_floor = new_total_floor_number
                    else:
                        new_floor = int(re.findall(pattern_floor, element_text)[0])
                        
                    if "sur" in element_text:
                        new_total_floor_number = int(re.findall(pattern_floor_number, element_text)[0])
                    else: 
                        new_total_floor_number = None
                
                #bedroom_number
                elif "chambre" in element_text:
                    new_bedroom_number = re.findall(regex_find_numbers, element_text)[0]
                
                # toilet_number
                elif "wc" in element_text:
                    if "séparé" in element_text:
                        continue
                    else:
                        new_toilet_number = re.findall(regex_find_numbers, element_text)[0]
                
                # bathroom_number
                elif "bain" in element_text:
                    new_bathroom_number = re.findall(regex_find_numbers, element_text)[0]
                
                #cellar
                elif "cave" in element_text:
                    new_cellar = True
                
                #lock_up_garage
                elif "box" in element_text:
                    new_lock_up_garage = True

                # heating
                elif "chauffage" in element_text:
                    new_heating = re.findall(regex_find_text_after_colon, element_text)[0]
                
                #tv_cable
                elif "tv" in element_text:
                    new_tv_cable = True
                
                #fireplace
                elif "cheminée" in element_text:
                    new_fireplace = True
                    
                #digicode
                elif "digicode" in element_text:
                    new_digicode = True
                    
                #intercom
                elif "interphone" in element_text:
                    new_intercom = True
                
                #elevator
                elif "ascenseur" in element_text:
                    new_elevator = True
                    
                #fibre_optics_status
                elif "fibre" in element_text:
                    new_fibre_optics_status = re.findall(regex_find_text_after_colon, element_text)[0].replace("*", "")

                # garden
                elif "jardin" in element_text:
                    new_garden = True
                    
                # car_park_number
                elif "parking" in element_text:
                    if functions.contains_numbers(element_text) == True:
                        new_car_park_number = re.findall(regex_find_numbers, element_text)[0]
                    else:
                        new_car_park_number = None
                
                #balcony
                elif "balcon" in element_text:
                    new_balcony = True
                    
                #large_balcony
                elif "terrasse" in element_text:
                    new_large_balcony = True
                
                #estate_agency_fee_percentage
                # elif "honoraires :" in element_text:
                #     pattern = r'[\d,]+%'
                #     estate_agency_fee_percentage = re.findall(pattern, element_text)[0].replace("%", "")
                
                #pinel
                elif "pinel" in element_text:
                    new_pinel = True
                    
                #denormandie
                elif "denormandie" in element_text:
                    new_pinel = True
                
                # announce_publication
                elif "publiée" in element_text:
                    if "il y a plus" in element_text:
                        new_announce_publication = None
                    else:
                        publication_french_date = re.findall(r'le\s(.+)', element_text)[0]
                        new_announce_publication = functions.date_converter_french_date_to_utc_timestamp(publication_french_date)
                
                # announce_last_modification
                elif "modifiée" in element_text:
                    modification_french_date = re.findall(r'le\s(.+)', element_text)[0]
                    new_announce_last_modification = functions.date_converter_french_date_to_utc_timestamp(modification_french_date)
                
                #dpe_date
                elif "dpe" in element_text:
                    dpe_french_date = re.findall(regex_find_text_after_colon, element_text)[0]
                    new_dpe_date = functions.date_converter_french_date_to_utc_timestamp(dpe_french_date)
                    
                #batch
                # elif "lot" in element_text:
                #     batch = re.findall(regex_find_numbers, element_text)[0]
                    
                else:
                    continue
                
            except(NoSuchElementException, StaleElementReferenceException):
                print("KO : no data elements found")

        print('step4')
        # neighborhood_description
        try: 
            neighborhood_description = driver.find_element(By.CSS_SELECTOR, "div.neighborhoodDescription span")
            new_neighborhood_description = neighborhood_description.text
        except(NoSuchElementException, StaleElementReferenceException):
                    print("KO : no data for neighborhood_description")
        
        # energetic_performance_letter
        try: 
            energetic_performance_letter = driver.find_element(By.CSS_SELECTOR, "div.dpe-line__classification span div")
            new_energetic_performance_letter = energetic_performance_letter.text
        except(NoSuchElementException, StaleElementReferenceException):
                    print("KO : no data for energetic_performance_letter")        
                    
        # energetic_performance_number && climatic_performance_number
        try: 
            dpe_data_numbers = driver.find_elements(By.CSS_SELECTOR, "div.dpe-data div.value span")
            if dpe_data_numbers:
                if dpe_data_numbers[0].text == "-": 
                    new_energetic_performance_number = None
                else:
                    new_energetic_performance_number = int(dpe_data_numbers[0].text)
                
                if dpe_data_numbers[1].text == "-": 
                    new_climatic_performance_number = None
                else:
                    new_climatic_performance_number = int(dpe_data_numbers[1].text.replace("*", ""))
            
        except(NoSuchElementException, StaleElementReferenceException):
                    print("KO : no data for energetic_performance_number")

        # climatic_performance_letter
        try: 
            new_climatic_performance_letter = driver.find_element(By.CSS_SELECTOR, "div.ges-line__classification span")
            new_climatic_performance_letter = new_climatic_performance_letter.text
        except(NoSuchElementException, StaleElementReferenceException):
                    print("KO : no data for climatic_performance_letter") 

        print("#############RECAP ANNOUNCE VARIABLES#############")
        print("year_of_construction         :",new_year_of_construction)
        print("exposition                   :",new_exposition)
        print("floor                        :",new_floor)
        print("total_floor_number           :",new_total_floor_number)
        print("neighborhood_description     :",new_neighborhood_description)  
        print("bedroom_number               :",new_bedroom_number)
        print("toilet_number                :",new_toilet_number)
        print("bathroom_number              :",new_bathroom_number)
        print("cellar                       :",new_cellar)
        print("lock_up_garage               :",new_lock_up_garage)
        print("heating                      :",new_heating)
        print("tv_cable                     :",new_tv_cable)
        print("fireplace                    :",new_fireplace) 
        print("digicode                     :",new_digicode)
        print("intercom                     :",new_intercom)
        print("elevator                     :",new_elevator)
        print("fibre_optics_status          :",new_fibre_optics_status) 
        print("garden                       :",new_garden)
        print("car_park_number              :",new_car_park_number)
        print("balcony                      :",new_balcony)
        print("large_balcony                :",new_large_balcony)
        print("dpe_date                     :",new_dpe_date)
        print("estate_agency_fee_percentage :",new_estate_agency_fee_percentage)
        print("pinel                        :",new_pinel)
        print("denormandie                  :",new_denormandie)
        print("announce_publication         :",new_announce_publication)
        print("announce_last_modification   :",new_announce_last_modification)
        print("energetic_performance_letter :",new_energetic_performance_letter)
        print("energetic_performance_number :",new_energetic_performance_number)
        print("climatic_performance_number  :",new_climatic_performance_number)
        print("climatic_performance_letter  :",new_climatic_performance_letter)
        
        print("------------------Description Part End------------------")
        
        if dateOfModification_announce != new_announce_last_modification:
            ###default values
            ##building options
            year_of_construction = ""
            exposition = ""
            floor = None
            total_floor_number = None
            neighborhood_description = ""

            ##rooms
            bedroom_number = 0
            toilet_number = 0
            bathroom_number = 0
            cellar = False
            lock_up_garage = False

            ##options indoor
            heating = ""
            tv_cable = False
            fireplace = False
            digicode = False
            intercom = False
            elevator = False
            fibre_optics_status = ""

            #options outdoor
            garden = False
            car_park_number = 0
            balcony = False
            large_balcony = False

            ##administration
            estate_agency_fee_percentage = 0
            pinel = False
            denormandie = False
            announce_publication = ""
            announce_last_modification = ""
            
            ##diagnostics
            dpe_date = ""
            energetic_performance_letter = None
            energetic_performance_number = 0 
            climatic_performance_number = 0
            climatic_performance_letter = None    
        
        
        # timestamp_difference = current_time_utc - dateOfModification_announce
        # days_difference = timestamp_difference / (60 * 60 * 24)
        # print("days_difference",days_difference)
        
        # if int(days_difference) > 7:
        #     print("url_property", url_property) 
        ###TODO check if the date of modification is different from the one registered
        ###TODO do not forget to implement an history of the price