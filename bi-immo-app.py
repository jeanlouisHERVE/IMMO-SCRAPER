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

#get data from .env file 
load_dotenv()

#variables
url_immo_website = os.environ["URL_IMMO_WEBSITE_BI"]
driver = webdriver.Chrome()
actions = ActionChains(driver)
chrome_options = ChromeOptions()
city_researched_content = os.environ["CITY_RESEARCHED_CONTENT"]
global_page_number = 2
current_time_utc = datetime.datetime.now(tz=pytz.utc).timestamp()

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

time.sleep(5)

# while True:
#     try:
#         next_results_btn = driver.find_element(By.CSS_SELECTOR, "a.btn.goForward.btn-primary.pagination__go-forward-button")
#     except(NoSuchElementException):
#         print("KO : no more next button")
#         break
    
#     articles = driver.find_elements(By.CSS_SELECTOR, "article.sideListItem")
#     print(f"------------------Page_Start {global_page_number-1}------------------")
#     print("articles",articles)
#     for article in articles:
#         print("------------------Article Start------------------")
#         print("article :", article)
        
#         ###type of property
#         type_of_property = ""
#         try:
#             type_of_property_content = article.find_element(By.CSS_SELECTOR,"span.ad-overview-details__ad-title")
#             type_of_property_content = type_of_property_content.text
#             if "maison" in  type_of_property_content.lower():
#                 type_of_property = "maison"
#             elif "appartement" in type_of_property_content.lower():
#                 type_of_property = "appartement"
#             else:   
#                 type_of_property = ""
#             print("type_of_property :",type_of_property)
            
#         except(NoSuchElementException):
#             print("KO : no data for type_of_property found")
        
#         ###town
#         town = os.environ["CITY_RESEARCHED"]
#         print("town :",town)
        
#         ###District&&Postcode
#         district = ""
#         postcode = 0
#         try: 
#             address_content = article.find_element(By.CSS_SELECTOR,"span.ad-overview-details__address-title")
#             address_content = address_content.text
#             ##district
#             try: 
#                 district = re.findall("\((.*?)\)", address_content)[0]
#             except IndexError:
#                 print("KO : no data for District found")
#                 distric = ""
#             ##postcode
#             try:
#                 postcode = re.findall("[0-9]*", address_content)[0]
#             except IndexError:
#                 print("KO : no data for Postcode found")
#                 postcode = 0
#             print("district :",district)
#             print("postcode :",postcode)
            
#         except(NoSuchElementException):
#             print("KO : no data for District&&Postcode found")
        
#         ###url
#         url = ""
#         try:
#             url_content = article.find_element(By.CSS_SELECTOR,"a.detailedSheetLink")
#             url = url_content.get_attribute('href')
#             print("link :",url)
#         except(NoSuchElementException):
#             print("KO : no data for url found")    
        
#         ###room number && surface
#         surface = 0
#         room_number = 0
#         try:
#             room_surface_content = article.find_element(By.CSS_SELECTOR,"span.ad-overview-details__ad-title")
#             content_text = room_surface_content.text
#             ##room
#             room_number = room_surface_content.text
#             pattern_room = r'(\d+)\s*pièce'
#             room_content = re.findall(pattern_room, content_text)
#             room_number = room_content[0]
#             print("room_number :",room_number)
#             ##surface
#             surface = room_surface_content.text
#             pattern_squaremeters = r'\b(\d+)\b'
#             surface_content = re.findall(pattern_squaremeters, content_text)
#             surface = surface_content[-1]
#             print("surface :",surface)
#         except(NoSuchElementException):
#             print("KO : no data for room number && surface found")
                
#         ###price
#         price = 0
#         try:
#             price_content = article.find_element(By.CSS_SELECTOR,"span.ad-price__the-price")
#             price_content = price_content.text
#             price = ''.join(re.findall('\d+', price_content))
#             if len(price) > 7:
#                 price = None
#             print("price :",price)
#         except(NoSuchElementException):
#             print("KO : no data for price found")
                
#         ###date 
#         date_add_to_db = current_time_utc
#         print("date_add_to_db :",date_add_to_db)
            
#         print("------------------Article End------------------")  
            
#         ###add properties to db
#         if not database.get_property_by_url(url):
#             database.add_property(type_of_property, town, district, postcode, url, room_number, surface, price, date_add_to_db)
            
        
        
#     ###catch data to access the next page
#     next_page_url = next_results_btn.get_attribute('href')
#     print("next_page_url", next_page_url)
#     pattern_next_page_url_without_page = r"(.+)\?"
#     next_page_url_without_page = re.findall(pattern_next_page_url_without_page, next_page_url)[0]
#     print("next_page_url_without_page :",next_page_url_without_page)
#     # patter_page_number = r"\bpage=(\d+)\b"
#     # page_number = re.findall(patter_page_number, next_page_url)[0]
#     # page_number = int(page_number)
#     # print("page_number :",page_number)
    
#     # driver.get(next_page_url_without_page +"page={}".format(global_page_number))
#     driver.get(next_page_url)
#     global_page_number += 1  
#     print("------------------Page_End------------------")


print("------------------Description Part------------------")
###Add description to database
property_urls = database.get_id_url_from_properties()
for id_property, url_property in property_urls:
    driver.get(url_property)
    
    
    labelsInfo = driver.find_elements(By.CSS_SELECTOR, "div.labelInfo")
    
    #default values
    bedroom_number = 0
    garden = False
    toilet_number = 0
    car_park_number = 0
    heating = ""
    year_of_construction = ""
    bathroom_number = 0
    fibre_optics_status = 0
    cellar = False
    
    for labelInfo in labelsInfo:
        
        try:
            element = labelInfo.find_element(By.CSS_SELECTOR, "span")
            element_text = element.text.lower()
            #bedroom_number
            if "chambre" in element_text:
                bedroom_regex = ""##############
                ######
                print("bedroom_number", bedroom_number)
            # garden
            elif "jardin" in element_text:
                garden = True
            
            # toilet_number
            elif "wc" in element_text:
                toilet_regex = ""
                ######
                print("toilet_number", toilet_number)
                
            # car_park_number
            elif "parking" in element_text:
                car_park_regex = ""
                ######
                print("car_park_number", car_park_number)
            
            # heating
            elif "chauffage" in element_text:
                heating_regex = ""
                ######
                print("heating", heating)
                
            # year_of_construction
            elif "construit" in element_text:
                construction_regex = ""
                ######
                print("year_of_construction", year_of_construction)
            
            # bathroom_number
            elif "bain" in element_text:
                bathroom_regex = ""
                ######
                print("bathroom_number", bathroom_number)
            
            #fibre_optics_status
            elif "fibre" in element_text:
                fibre_regex = ""
                ######
                print("fibre_optics_status", fibre_optics_status)
                
            #cellar
            elif "cave" in element_text:
                cellar = True
                print("cellar", cellar)
            
            # floor
            elif "étage" in element_text:
                cellar = True
                print("cellar", cellar)
            fi
            
            
            print("element.text", element.text)
        except(NoSuchElementException, StaleElementReferenceException):
             print("KO : no data elements found")
    input()
    
    # exposition
    
    
    #fibre_optics_status
    
    
    
    
    
    # dpe_date
    
    # energetic_performance_letter
    energetic_performance_letter = ""
    try: 
        energetic_performance_letter = driver.find_element(By.CSS_SELECTOR, "div.dpe-line__classification span div")
        energetic_performance_letter = energetic_performance_letter.text
    except(NoSuchElementException, StaleElementReferenceException):
             print("KO : no data for energetic_performance_letter")
    print("energetic_performance_letter",energetic_performance_letter)         
             
    # energetic_performance_number && climatic_performance_number
    energetic_performance_number = 0 
    climatic_performance_number = 0
    try: 
        dpe_data_numbers = driver.find_elements(By.CSS_SELECTOR, "div.dpe-data span div")
        if dpe_data_numbers:
            energetic_performance_number = int(dpe_data_numbers[0].text)
            climatic_performance_number = int(dpe_data_numbers[1].text)
    except(NoSuchElementException, StaleElementReferenceException):
             print("KO : no data for energetic_performance_number")
    print("energetic_performance_number", energetic_performance_number) 
    print("climatic_performance_number", climatic_performance_number) 
    
    # climatic_performance_letter
    climatic_performance_letter = ""
    try: 
        climatic_performance_letter = driver.find_element(By.CSS_SELECTOR, "div.ges-line__classification span")
        climatic_performance_letter = climatic_performance_letter.text
    except(NoSuchElementException, StaleElementReferenceException):
             print("KO : no data for climatic_performance_letter")
    print("climatic_performance_letter",climatic_performance_letter)  
    
    # announce_publication
    # announce_last_modification
    
    # neighborhood_description
    neighborhood_description = ""
    try: 
        neighborhood_description = driver.find_element(By.CSS_SELECTOR, "div.neighborhoodDescription span")
        neighborhood_description = neighborhood_description.text
    except(NoSuchElementException, StaleElementReferenceException):
             print("KO : no data for neighborhood_description")
    print("neighborhood_description",neighborhood_description) 
    
    # estate_agency 
    estate_agency  = ""
    try: 
        estate_agency  = driver.find_element(By.CSS_SELECTOR, "div.agency-overview__info-name")
        estate_agency  = estate_agency.text
        if database.get_agency(estate_agency):
            database.add_agency()
    except(NoSuchElementException, StaleElementReferenceException):
             print("KO : no data for estate_agency ")
    print("estate_agency ",estate_agency )
    
