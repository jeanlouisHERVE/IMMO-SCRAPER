# packages
import os
import re
import time
import pytz
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException
    )
from selenium.webdriver.common.action_chains import ActionChains

# other modules
from dotenv import load_dotenv
from driver_manager import WebDriverManager

# own packages
import database_app
import functions

# get data from .env file
load_dotenv()

# variables
driver = WebDriverManager.get_driver()
actions = ActionChains(driver)
url_immo_website = os.environ["URL_IMMO_WEBSITE_BI"]
city_researched_content = os.environ["CITY_RESEARCHED_CONTENT"]
current_time_utc = datetime.datetime.now(tz=pytz.utc).timestamp()
functions = functions


# functions
def check_accept_section(cssSelector: str):

    driver.implicitly_wait(5)
    try:
        accept = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, cssSelector))
                )
        accept.click()
    except (
        NoSuchElementException,
        StaleElementReferenceException,
        TimeoutException
    ):
        print("KO : no accept part")


def add_new_announces():

    global_page_number = 2

    print("------------------Add_new_annouces_Start------------------")
    # connection to website
    driver.get(url_immo_website)
    driver.implicitly_wait(5)
    # check an agree the terms section exists
    time.sleep(2)
    check_accept_section('span.didomi-continue-without-agreeing')
    time.sleep(2)

    # fill research section
    search_input = driver.find_element(By.CSS_SELECTOR, "input.tt-input")
    search_input.send_keys(os.environ["CITY_RESEARCHED"])
    time.sleep(2)

    # select desired town in the dropdown menu
    try:
        dropdown_element = driver.find_elements(By.CSS_SELECTOR, "div.suggestionItem")[0]
        time.sleep(2)
        actions.click(dropdown_element).perform()
    except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
        print("KO : unable to make the dropdown menu appear")

    # click on the search button
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.search").click()
    annonce = 0

    while True:
        try:
            next_results_btn = driver.find_element(
                                By.CSS_SELECTOR, "a.btn.goForward.btn-primary.pagination__go-forward-button"
                                )
        except (NoSuchElementException):
            print("KO : no more next button")
            break

        articles = driver.find_elements(
                                By.CSS_SELECTOR, "article.sideListItem"
                                )
        print(f"------------------Page_Start {global_page_number-1}------------------")
        print("articles", articles)
        for article in articles:
            print(f"{article} {annonce}")
            annonce += 1
            print("------------------Article Start------------------")
            print("article :", article)

            # type of property
            type_of_property = ""
            try:
                type_of_property_content = article.find_element(
                                                    By.CSS_SELECTOR, "span.ad-overview-details__ad-title"
                                                    )
                type_of_property_content = type_of_property_content.text
                if "maison" in type_of_property_content.lower():
                    type_of_property = "maison"
                elif "appartement" in type_of_property_content.lower():
                    type_of_property = "appartement"
                else:
                    type_of_property = ""
                print("type_of_property :", type_of_property)

            except (NoSuchElementException):
                print("KO : no data for type_of_property found")

            # town
            town = os.environ["CITY_RESEARCHED"]
            print("town :", town)

            # District&&Postcode
            district = ""
            postcode = 0
            try:
                address_content = article.find_element(
                                        By.CSS_SELECTOR, "span.ad-overview-details__address-title"
                                        )
                address_content = address_content.text
                # district
                try:
                    district = re.findall(r"\((.*?)\)", address_content)[0]
                except IndexError:
                    print("KO : no data for District found")
                    district = ""
                # postcode
                try:
                    postcode = re.findall(r"[0-9]*", address_content)[0]
                except IndexError:
                    print("KO : no data for Postcode found")
                    postcode = 0
                print("district :", district)
                print("postcode :", postcode)

            except (NoSuchElementException):
                print("KO : no data for District&&Postcode found")

            # url
            url = ""
            try:
                url_content = article.find_element(By.CSS_SELECTOR, "a.detailedSheetLink")
                url = url_content.get_attribute('href')
                print("link :", url)
            except (NoSuchElementException):
                print("KO : no data for url found")

            # room number && surface
            surface = 0
            room_number = 0
            try:
                room_surface_content = article.find_element(
                                                    By.CSS_SELECTOR, "span.ad-overview-details__ad-title"
                                                    )
                content_text = room_surface_content.text
                # room
                room_number = room_surface_content.text
                pattern_room = r'(\d+)\s*pièce'
                room_content = re.findall(pattern_room, content_text)
                room_number = room_content[0]
                print("room_number :", room_number)
                # surface
                surface = room_surface_content.text
                pattern_squaremeters = r'\b(\d+)\b'
                surface_content = re.findall(pattern_squaremeters, content_text)
                surface = surface_content[-1]
                print("surface :", surface)
            except (NoSuchElementException):
                print("KO : no data for room number && surface found")

            # price
            price = 0
            try:
                price_content = article.find_element(By.CSS_SELECTOR, "span.ad-price__the-price")
                price_content = price_content.text
                price = ''.join(re.findall(r'\d+', price_content))
                if len(price) > 7:
                    price = None
                print("price :", price)
            except (NoSuchElementException):
                print("KO : no data for price found")

            # date
            date_add_to_db = current_time_utc
            print("date_add_to_db :", date_add_to_db)

            print("------------------Article End------------------")

            # add properties to db
            if not database_app.get_property_by_url(url):
                property_id = database_app.add_property(
                                                    type_of_property,
                                                    town,
                                                    district,
                                                    postcode,
                                                    url,
                                                    room_number,
                                                    surface,
                                                    date_add_to_db
                                                    )
                database_app.add_price_to_property(date_add_to_db, property_id, price)

        # catch data to access the next page
        next_page_url = next_results_btn.get_attribute('href')
        print("next_page_url", next_page_url)
        pattern_next_page_url_without_page = r"(.+)\?"
        next_page_url_without_page = re.findall(pattern_next_page_url_without_page, next_page_url)[0]
        print("next_page_url_without_page :", next_page_url_without_page)
        driver.get(next_page_url)
        global_page_number += 1
        print("------------------Add_new_annouces_End------------------")


def add_descriptions():
    print("------------------DESCRIPTION PART------------------")
    # Add description to database
    property_urls = database_app.get_id_url_from_properties()

    for id_property, url_property in property_urls:

        print(f"------------------Start add description {id_property}------------------")
        print("url_property", url_property)
        # check if the property has or not a description linked
        if not database_app.get_property_description_by_id(id_property):

            driver.get(url_property)
            driver.implicitly_wait(5)

            # check if a agreeing pop-up displays
            check_accept_section('span.didomi-continue-without-agreeing')
            driver.implicitly_wait(5)

            # check if the announce is still available
            try:
                outOfTheMarket = driver.find_element(By.CLASS_NAME, "outOfTheMarketBanner")
                print(f"KO : Announce no more available {outOfTheMarket}")
                database_app.delete_property(id_property)
                continue
            except (NoSuchElementException):
                print("OK : Announce still available")

                labelsInfo = driver.find_elements(By.CSS_SELECTOR, "div.labelInfo")

                # default values
                # building options
                year_of_construction = ""
                exposition = ""
                floor = None
                total_floor_number = None
                neighborhood_description = ""

                # rooms
                bedroom_number = 0
                toilet_number = 0
                bathroom_number = 0
                cellar = False
                lock_up_garage = False

                # options indoor
                heating = ""
                tv_cable = False
                fireplace = False
                digicode = False
                intercom = False
                elevator = False
                fibre_optics_status = ""

                # options outdoor
                garden = False
                car_park_number = 0
                balcony = False
                large_balcony = False

                # administration
                estate_agency_fee_percentage = 0
                pinel = False
                denormandie = False
                announce_publication = ""
                announce_last_modification = current_time_utc

                # diagnostics
                dpe_date = ""
                energetic_performance_letter = None
                energetic_performance_number = 0
                climatic_performance_number = 0
                climatic_performance_letter = None

                regex_find_numbers = r'\d+'
                regex_find_text_after_colon = r':\s*([^:,]+)'

                driver.implicitly_wait(5)
                for labelInfo in labelsInfo:
                    try:
                        element = labelInfo.find_element(By.CSS_SELECTOR, "span")
                        element_text = element.text.lower()

                        # year_of_construction
                        if "construit" in element_text:
                            year_of_construction = re.findall(regex_find_numbers, element_text)[0]
                            format_string_construction = "%Y"
                            local_timestamp_construction = datetime.datetime.strptime(
                                                                            year_of_construction,
                                                                            format_string_construction
                                                                            )
                            year_of_construction = local_timestamp_construction.replace(
                                                                                tzinfo=pytz.timezone('UTC')
                                                                                ).timestamp()

                        # exposition
                        elif "exposé" in element_text:
                            pattern_exposition = r'exposé\s(.+)'
                            exposition = re.findall(pattern_exposition, element_text)[0]

                        # floor
                        # total_floor_number
                        elif "étage" in element_text:
                            pattern_floor = r'^[0-9]+'
                            pattern_floor_number = r'sur\s+(\d+)'

                            if "dernier" in element_text:
                                floor = total_floor_number
                            else:
                                floor = int(re.findall(pattern_floor, element_text)[0])

                            if "sur" in element_text:
                                total_floor_number = int(re.findall(pattern_floor_number, element_text)[0])
                            else:
                                total_floor_number = None

                        # bedroom_number
                        elif "chambre" in element_text:
                            bedroom_number = re.findall(regex_find_numbers, element_text)[0]

                        # toilet_number
                        elif "wc" in element_text:
                            if "séparé" in element_text:
                                continue
                            else:
                                toilet_number = re.findall(regex_find_numbers, element_text)[0]

                        # bathroom_number
                        elif "bain" in element_text:
                            bathroom_number = re.findall(regex_find_numbers, element_text)[0]

                        # cellar
                        elif "cave" in element_text:
                            cellar = True

                        # lock_up_garage
                        elif "box" in element_text:
                            lock_up_garage = True

                        # heating
                        elif "chauffage" in element_text:
                            heating = re.findall(regex_find_text_after_colon, element_text)[0]

                        # tv_cable
                        elif "tv" in element_text:
                            tv_cable = True

                        # fireplace
                        elif "cheminée" in element_text:
                            fireplace = True

                        # digicode
                        elif "digicode" in element_text:
                            digicode = True

                        # intercom
                        elif "interphone" in element_text:
                            intercom = True

                        # elevator
                        elif "ascenseur" in element_text:
                            elevator = True

                        # fibre_optics_status
                        elif "fibre" in element_text:
                            fibre_optics_status = re.findall(
                                                    regex_find_text_after_colon,
                                                    element_text
                                                    )[0].replace("*", "")

                        # garden
                        elif "jardin" in element_text:
                            garden = True

                        # car_park_number
                        elif "parking" in element_text:
                            if functions.contains_numbers(element_text) is True:
                                car_park_number = re.findall(regex_find_numbers, element_text)[0]
                            else:
                                car_park_number = None

                        # balcony
                        elif "balcon" in element_text:
                            balcony = True

                        # large_balcony
                        elif "terrasse" in element_text:
                            large_balcony = True

                        # estate_agency_fee_percentage
                        #  elif "honoraires :" in element_text:
                        #      pattern = r'[\d,]+%'
                        #      estate_agency_fee_percentage = re.findall(
                            #                                             pattern,
                            #                                             element_text
                            #                                            )[0].replace("%", "")

                        # pinel
                        elif "pinel" in element_text:
                            pinel = True

                        # denormandie
                        elif "denormandie" in element_text:
                            pinel = True

                        # announce_publication
                        elif "publiée" in element_text:
                            if "il y a plus" in element_text:
                                announce_publication = None
                            else:
                                publication_french_date = re.findall(r'le\s(.+)', element_text)[0]
                                announce_publication = functions.date_converter_french_date_to_utc_timestamp(
                                                                                    publication_french_date
                                                                                    )

                        # announce_last_modification
                        elif "modifiée" in element_text:
                            modification_french_date = re.findall(r'le\s(.+)', element_text)[0]
                            announce_last_modification = functions.date_converter_french_date_to_utc_timestamp(
                                                                                    modification_french_date
                                                                                    )

                        # dpe_date
                        elif "dpe" in element_text:
                            dpe_french_date = re.findall(regex_find_text_after_colon, element_text)[0]
                            dpe_date = functions.date_converter_french_date_to_utc_timestamp(dpe_french_date)

                        # batch
                        #  elif "lot" in element_text:
                        #      batch = re.findall(regex_find_numbers, element_text)[0]

                        else:
                            continue

                    except (NoSuchElementException, StaleElementReferenceException):
                        print("KO : no data elements found")

                # neighborhood_description
                try:
                    neighborhood_description = driver.find_element(
                                                                By.CSS_SELECTOR,
                                                                "div.neighborhoodDescription span"
                                                                )
                    neighborhood_description = neighborhood_description.text
                except (NoSuchElementException, StaleElementReferenceException):
                    print("KO : no data for neighborhood_description")

                # energetic_performance_letter
                try:
                    energetic_performance_letter = driver.find_element(
                                                                By.CSS_SELECTOR,
                                                                "div.dpe-line__classification span div"
                                                                )
                    energetic_performance_letter = energetic_performance_letter.text
                except (NoSuchElementException, StaleElementReferenceException):
                    print("KO : no data for energetic_performance_letter")

                # energetic_performance_number && climatic_performance_number
                try:
                    dpe_data_numbers = driver.find_elements(
                                                        By.CSS_SELECTOR,
                                                        "div.dpe-data div.value span"
                                                        )
                    if dpe_data_numbers:
                        if dpe_data_numbers[0].text == "-":
                            energetic_performance_number = None
                        else:
                            energetic_performance_number = int(dpe_data_numbers[0].text)

                        if dpe_data_numbers[1].text == "-":
                            climatic_performance_number = None
                        else:
                            climatic_performance_number = int(dpe_data_numbers[1].text.replace("*", ""))

                except (NoSuchElementException, StaleElementReferenceException):
                    print("KO : no data for energetic_performance_number")

                # climatic_performance_letter
                try:
                    climatic_performance_letter = driver.find_element(By.CSS_SELECTOR,
                                                                      "div.ges-line__classification span"
                                                                      )
                    climatic_performance_letter = climatic_performance_letter.text
                except (NoSuchElementException, StaleElementReferenceException):
                    print("KO : no data for climatic_performance_letter")

                print("------------------Description Part End------------------")
                print("--------------------------------------------------------")
                print("----------------------Agency Part-----------------------")

                # estate_agency
                estate_agency_name = ""
                estate_agency_address = ""
                estate_agency_evaluation = ""

                # name
                try:
                    estate_agency_name = driver.find_element(By.CSS_SELECTOR,
                                                             "div.agency-overview__info-name"
                                                             )
                    estate_agency_name = estate_agency_name.text
                except (NoSuchElementException, StaleElementReferenceException):
                    print("KO : no data for estate_agency name ")
                    estate_agency_name = None

                # address
                try:
                    estate_agency_address = driver.find_element(By.CSS_SELECTOR,
                                                                """div.agency-overview__contact-address
                                                                div.contact-address"""
                                                                )
                    estate_agency_address = estate_agency_address.text

                except (NoSuchElementException, StaleElementReferenceException):
                    print("KO : no data for estate_agency address")
                    estate_agency_address = None

                # fee_percentage
                # value caught above

                # evaluation
                try:
                    estate_agency_evaluation = driver.find_element(
                        By.CSS_SELECTOR,
                        "span.rating-stars__rating-text"
                    )
                    estate_agency_evaluation = estate_agency_evaluation.text
                except (NoSuchElementException, StaleElementReferenceException):
                    print("KO : no data for estate_agency evaluation")
                    estate_agency_evaluation = None

                print("estate_agency_name", estate_agency_name)
                print("estate_agency_address", estate_agency_address)
                print("estate_agency_fee_percentage", estate_agency_fee_percentage)
                print("estate_agency_evaluation", estate_agency_evaluation)

                result = database_app.get_agency_by_name(estate_agency_name)
                print("result", result)

                if not database_app.get_agency_by_name(estate_agency_name) or estate_agency_name is None:
                    print("stepagency1")
                    database_app.add_agency(estate_agency_name,
                                            estate_agency_address,
                                            estate_agency_fee_percentage,
                                            estate_agency_evaluation
                                            )
                    print("stepagency2")
                    print(f"OK : {estate_agency_name} estate_agency has been added to database")
                else:
                    print("stepagency3")
                    print(f"KO : {estate_agency_name} estate_agency already exits")

                try:
                    estate_agency_id = database_app.get_agency_id_from_name(estate_agency_name)[0][0]
                except IndexError:
                    if not estate_agency_id:
                        estate_agency_id = None

                print("estate_agency_id", estate_agency_id)
                print("------------------Agency Part End------------------")

                print(f"------------------Add Description {id_property}------------------")
                print("#############RECAP ANNOUNCE VARIABLES#############")
                print("year_of_construction         :", year_of_construction)
                print("exposition                   :", exposition)
                print("floor                        :", floor)
                print("total_floor_number           :", total_floor_number)
                print("neighborhood_description     :", neighborhood_description)
                print("bedroom_number               :", bedroom_number)
                print("toilet_number                :", toilet_number)
                print("bathroom_number              :", bathroom_number)
                print("cellar                       :", cellar)
                print("lock_up_garage               :", lock_up_garage)
                print("heating                      :", heating)
                print("tv_cable                     :", tv_cable)
                print("fireplace                    :", fireplace)
                print("digicode                     :", digicode)
                print("intercom                     :", intercom)
                print("elevator                     :", elevator)
                print("fibre_optics_status          :", fibre_optics_status)
                print("garden                       :", garden)
                print("car_park_number              :", car_park_number)
                print("balcony                      :", balcony)
                print("large_balcony                :", large_balcony)
                print("dpe_date                     :", dpe_date)
                print("estate_agency_fee_percentage :", estate_agency_fee_percentage)
                print("pinel                        :", pinel)
                print("denormandie                  :", denormandie)
                print("announce_publication         :", announce_publication)
                print("announce_last_modification   :", announce_last_modification)
                print("energetic_performance_letter :", energetic_performance_letter)
                print("energetic_performance_number :", energetic_performance_number)
                print("climatic_performance_number  :", climatic_performance_number)
                print("climatic_performance_letter  :", climatic_performance_letter)

                database_app.add_description(id_property,
                                             year_of_construction,
                                             exposition,
                                             floor,
                                             total_floor_number,
                                             neighborhood_description,
                                             bedroom_number,
                                             toilet_number,
                                             bathroom_number,
                                             cellar,
                                             lock_up_garage,
                                             heating,
                                             tv_cable,
                                             fireplace,
                                             digicode,
                                             intercom,
                                             elevator,
                                             fibre_optics_status,
                                             garden,
                                             car_park_number,
                                             balcony,
                                             large_balcony,
                                             estate_agency_fee_percentage,
                                             pinel,
                                             denormandie,
                                             announce_publication,
                                             announce_last_modification,
                                             dpe_date,
                                             energetic_performance_letter,
                                             energetic_performance_number,
                                             climatic_performance_number,
                                             climatic_performance_letter,
                                             estate_agency_id
                                             )

                print("------------------End Add Description------------------")

        else:
            print(f"OK : property {id_property} already has a description")
