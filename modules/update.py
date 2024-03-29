# packages
import os
import re
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
from driver_manager import WebDriverManager

# other modules
from dotenv import load_dotenv

# own packages
import database_app
import functions
import data

# get data from .env file
load_dotenv()

# variables
driver = WebDriverManager.get_driver()
url_immo_website = os.environ["URL_IMMO_WEBSITE_BI"]
city_researched_content = os.environ["CITY_RESEARCHED_CONTENT"]
current_time_utc = datetime.datetime.now(tz=pytz.utc).timestamp()
global announce_modified

# date
new_date_add_to_db = current_time_utc
print("new_date_add_to_db :", new_date_add_to_db)


# functions
def check_accept_section(cssSelector: str):
    driver.implicitly_wait(5)
    try:
        accept = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, cssSelector)))
        accept.click()
    except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
        print(f"{data.blue}KO : no accept part{data.white}")


def update_descriptions():
    # get data from properties already in database
    for property in database_app.get_id_url_dateofmodification_from_properties():
        id_property, url_property, dateOfModification_announce = property
        print("---------------------------------------START------------------------------------------")
        print(f"--------------------------------PROPERTY {id_property}--------------------------------")
        print("--------------------------------------------------------------------------------------")

        print("url_property", url_property)
        print("id_property", id_property, type(id_property))
        driver.get(url_property)
        driver.implicitly_wait(10)
        announce_modified = False

        check_accept_section('span.didomi-continue-without-agreeing')
        driver.implicitly_wait(5)

        # check if the announce is still available
        try:
            outOfTheMarket = driver.find_element(By.CLASS_NAME, "outOfTheMarketBanner")
            # if the announce is not available it's moved to old tables
            print("outOfTheMarket", outOfTheMarket)
            property_data = database_app.get_property_by_id(id_property)
            property_data = list(property_data)
            estate_agency_id = database_app.get_estate_agency_id_by_property_id(id_property)
            database_app.update_total_active_decrement(estate_agency_id)  # update agency total_announces_active
            del property_data[0]  # delete id
            print("property_data", property_data)
            type_of_property = property_data[0]
            town = property_data[1]
            district = property_data[2]
            postcode = property_data[3]
            url = property_data[4]
            room_number = property_data[5]
            surface = property_data[6]
            date_add_to_db = property_data[7]
            description_data = database_app.get_property_description_by_id(id_property)
            description_data = list(description_data)

            print("description_data", description_data, type(description_data))
            new_property_id = database_app.add_old_property(type_of_property,
                                                            town,
                                                            district,
                                                            postcode,
                                                            url,
                                                            room_number,
                                                            surface,
                                                            date_add_to_db)
            year_of_construction = description_data[1]
            exposition = description_data[2]
            floor = description_data[3]
            total_floor_number = description_data[4]
            neighborhood_description = description_data[5]
            bedroom_number = description_data[6]
            toilet_number = description_data[7]
            bathroom_number = description_data[8]
            cellar = description_data[9]
            lock_up_garage = description_data[10]
            heating = description_data[11]
            tv_cable = description_data[12]
            fireplace = description_data[13]
            digicode = description_data[14]
            intercom = description_data[15]
            elevator = description_data[16]
            fibre_optics_status = description_data[17]
            garden = description_data[18]
            car_park_number = description_data[19]
            balcony = description_data[20]
            large_balcony = description_data[21]
            estate_agency_fee_percentage = description_data[22]
            pinel = description_data[23]
            denormandie = description_data[24]
            announce_publication = description_data[25]
            announce_last_modification = description_data[26]
            dpe_date = description_data[27]
            energetic_performance_letter = description_data[28]
            energetic_performance_number = description_data[29]
            climatic_performance_number = description_data[30]
            climatic_performance_letter = description_data[31]
            estate_agency_id = description_data[32]

            print("new_property_id", new_property_id)
            database_app.add_old_description(new_property_id,
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
            print("id_property", type(id_property))

            old_prices = database_app.get_prices_by_property_id(id_property)
            for old_price in old_prices:
                old_price = list(old_price)
                del old_price[0]
                date, property_id, price = old_price
                database_app.add_old_price_to_old_property(date,
                                                           new_property_id,
                                                           price
                                                           )

            database_app.delete_property(int(id_property))
            continue
        except (NoSuchElementException):
            print(f"{data.blue}KO : no out of the market banner {data.white}")

        labelsInfo = driver.find_elements(By.CSS_SELECTOR, "div.labelInfo")

        new_price = 0

        # default values
        # building options
        new_year_of_construction = ""
        new_exposition = ""
        new_floor = None
        new_total_floor_number = None
        new_neighborhood_description = ""

        # rooms
        new_bedroom_number = 0
        new_toilet_number = 0
        new_bathroom_number = 0
        new_cellar = False
        new_lock_up_garage = False

        # options indoor
        new_heating = ""
        new_tv_cable = False
        new_fireplace = False
        new_digicode = False
        new_intercom = False
        new_elevator = False
        new_fibre_optics_status = ""

        # options outdoor
        new_garden = False
        new_car_park_number = 0
        new_balcony = False
        new_large_balcony = False

        # administration
        new_estate_agency_fee_percentage = 0
        new_pinel = False
        new_denormandie = False
        new_announce_publication = ""
        new_announce_last_modification = None

        # diagnostics
        new_dpe_date = ""
        new_energetic_performance_letter = None
        new_energetic_performance_number = 0
        new_climatic_performance_number = 0
        new_climatic_performance_letter = None

        regex_find_numbers = r'\d+'
        regex_find_text_after_colon = r':\s*([^:,]+)'
        last_price = database_app.get_last_price_for_property(id_property)
        # get new price

        try:
            price_elements = driver.find_elements(By.CSS_SELECTOR, "span.ad-price__the-price")

            if len(price_elements) == 1:
                for price_element in price_elements:
                    new_price_content = price_element.text
                    new_price_content = new_price_content.replace(" ", "")
                    new_price = re.findall(regex_find_numbers, new_price_content)[0]
                    new_price = float(new_price)
                    # Process the new_price as needed
            elif len(price_elements) > 1:
                raise ValueError(f"{data.red}KO: Multiple elements found for span.ad-price__the-price{data.white}")
            else:
                print(f"{data.blue}KO: No elements found for span.ad-price__the-price{data.white}")

        except NoSuchElementException:
            print(f"{data.red}KO: Error finding elements{data.white}")
        except ValueError as ve:
            print(str(ve))

        # get others data
        for labelInfo in labelsInfo:

            try:
                element = labelInfo.find_element(By.CSS_SELECTOR, "span")
                element_text = element.text.lower()
                print('element_text ', element_text)

                # year_of_construction
                if "construit" in element_text:
                    new_year_of_construction = re.findall(regex_find_numbers, element_text)[0]
                    format_string_construction = "%Y"
                    local_timestamp_construction = datetime.datetime.strptime(
                                                                    new_year_of_construction,
                                                                    format_string_construction
                                                                )
                    new_year_of_construction = local_timestamp_construction.replace(
                                                                                tzinfo=pytz.timezone('UTC')
                                                                            ).timestamp()

                # exposition
                elif "exposé" in element_text:
                    pattern_exposition = r'exposé\s(.+)'
                    new_exposition = re.findall(pattern_exposition, element_text)[0]

                # floor
                # total_floor_number
                elif "étage" in element_text:
                    pattern_floor = r'^[0-9]+'
                    pattern_floor_number = r'sur\s+(\d+)'

                    if "dernier" in element_text:
                        new_floor = new_total_floor_number
                    else:
                        new_floor = int(re.findall(pattern_floor, element_text)[0])

                    if "sur" in element_text:
                        new_total_floor_number = int(re.findall(
                                                        pattern_floor_number,
                                                        element_text)[0]
                                                     )
                    else:
                        new_total_floor_number = None

                # bedroom_number
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

                # cellar
                elif "cave" in element_text:
                    new_cellar = True

                # lock_up_garage
                elif "box" in element_text:
                    new_lock_up_garage = True

                # heating
                elif "chauffage" in element_text:
                    new_heating = re.findall(regex_find_text_after_colon, element_text)[0]

                # tv_cable
                elif "tv" in element_text:
                    new_tv_cable = True

                # ireplace
                elif "cheminée" in element_text:
                    new_fireplace = True

                # digicode
                elif "digicode" in element_text:
                    new_digicode = True

                # intercom
                elif "interphone" in element_text:
                    new_intercom = True

                # elevator
                elif "ascenseur" in element_text:
                    new_elevator = True

                # fibre_optics_status
                elif "fibre" in element_text:
                    new_fibre_optics_status = re.findall(regex_find_text_after_colon,
                                                         element_text)[0].replace("*", "")

                # garden
                elif "jardin" in element_text:
                    new_garden = True

                # car_park_number
                elif "parking" in element_text:
                    if functions.contains_numbers(element_text):
                        new_car_park_number = re.findall(regex_find_numbers, element_text)[0]
                    else:
                        new_car_park_number = None

                # balcony
                elif "balcon" in element_text:
                    new_balcony = True

                # large_balcony
                elif "terrasse" in element_text:
                    new_large_balcony = True

                # estate_agency_fee_percentage
                # elif "honoraires :" in element_text:
                #     pattern = r'[\d,]+%'
                #     estate_agency_fee_percentage = re.findall(pattern, element_text)[0].replace("%", "")

                # pinel
                elif "pinel" in element_text:
                    new_pinel = True

                # denormandie
                elif "denormandie" in element_text:
                    new_pinel = True

                # announce_publication
                elif "publiée" in element_text:
                    if "il y a plus" in element_text:
                        new_announce_publication = None
                    else:
                        new_publication_french_date = re.findall(r'le\s(.+)', element_text)[0]
                        new_announce_publication = functions.date_converter_french_date_to_utc_timestamp(
                                                                                new_publication_french_date
                                                                                )
                        new_announce_publication = functions.date_converter_french_date_to_utc_timestamp(
                                                                                new_publication_french_date
                                                                                )

                # announce_last_modification
                elif "modifiée" in element_text:
                    new_modification_french_date = re.findall(r'le\s(.+)', element_text)[0]
                    new_announce_last_modification = functions.date_converter_french_date_to_utc_timestamp(
                                                                                new_modification_french_date
                                                                                )

                # dpe_date
                elif "dpe" in element_text:
                    new_dpe_french_date = re.findall(regex_find_text_after_colon, element_text)[0]
                    new_dpe_date = functions.date_converter_french_date_to_utc_timestamp(new_dpe_french_date)

                # batch
                # elif "lot" in element_text:
                #     batch = re.findall(regex_find_numbers, element_text)[0]

                else:
                    continue

            except (NoSuchElementException, StaleElementReferenceException):
                print(f"{data.red}KO : no data elements found{data.white}")

        # neighborhood_description
        try:
            new_neighborhood_description = driver.find_element(
                                                        By.CSS_SELECTOR,
                                                        "div.neighborhoodDescription span"
                                                    )
            new_neighborhood_description = new_neighborhood_description.text
        except (NoSuchElementException, StaleElementReferenceException):
            print(f"{data.blue}KO : no data for neighborhood_description{data.white}")

        # energetic_performance_letter
        try:
            new_energetic_performance_letter = driver.find_element(
                                                        By.CSS_SELECTOR,
                                                        "div.dpe-line__classification span div"
                                                    )
            new_energetic_performance_letter = new_energetic_performance_letter.text
        except (NoSuchElementException, StaleElementReferenceException):
            print(f"{data.blue}KO : no data for energetic_performance_letter{data.white}")

        # energetic_performance_number && climatic_performance_number
        try:
            new_dpe_data_numbers = driver.find_elements(
                                                    By.CSS_SELECTOR,
                                                    "div.dpe-data div.value span"
                                                )
            if new_dpe_data_numbers:
                if new_dpe_data_numbers[0].text == "-":
                    new_energetic_performance_number = None
                else:
                    new_energetic_performance_number = int(new_dpe_data_numbers[0].text)

                if new_dpe_data_numbers[1].text == "-":
                    new_climatic_performance_number = None
                else:
                    new_climatic_performance_number = int(new_dpe_data_numbers[1].text.replace("*", ""))

        except (NoSuchElementException, StaleElementReferenceException):
            print(f"{data.blue}KO : no data for energetic_performance_number{data.white}")

        # climatic_performance_letter
        try:
            new_climatic_performance_letter = driver.find_element(
                                                        By.CSS_SELECTOR, "div.ges-line__classification span"
                                                        )
            new_climatic_performance_letter = new_climatic_performance_letter.text
        except (NoSuchElementException, StaleElementReferenceException):
            print(f"{data.blue}KO : no data for climatic_performance_letter{data.white}")

        print("------------------Description Part End------------------")

        # update announce based on the modification date
        print("last_price", last_price)
        print('new_price', new_price)
        if new_price is None or last_price is new_price:
            print(f"{data.blue}KO : New price is the same than the old one{data.white}")
            continue
        else:
            # default values
            # building options
            old_property_description = database_app.get_property_description_by_id(id_property)
            year_of_construction = old_property_description[1]
            exposition = old_property_description[2]
            floor = old_property_description[3]
            total_floor_number = old_property_description[4]
            neighborhood_description = old_property_description[5]
            bedroom_number = old_property_description[6]
            toilet_number = old_property_description[7]
            bathroom_number = old_property_description[8]
            cellar = old_property_description[9]
            lock_up_garage = old_property_description[10]
            heating = old_property_description[11]
            tv_cable = old_property_description[12]
            fireplace = old_property_description[13]
            digicode = old_property_description[14]
            intercom = old_property_description[15]
            elevator = old_property_description[16]
            fibre_optics_status = old_property_description[17]
            garden = old_property_description[18]
            car_park_number = old_property_description[19]
            balcony = old_property_description[20]
            large_balcony = old_property_description[21]
            estate_agency_fee_percentage = old_property_description[22]
            pinel = old_property_description[23]
            denormandie = old_property_description[24]
            announce_publication = old_property_description[25]
            announce_last_modification = old_property_description[26]
            dpe_date = old_property_description[27]
            energetic_performance_letter = old_property_description[28]
            energetic_performance_number = old_property_description[29]
            climatic_performance_number = old_property_description[30]
            climatic_performance_letter = old_property_description[31]
            estate_agency_id = old_property_description[32]
            print("#############RECAP ANNOUNCE VARIABLES#############")
            print("price                        :", new_price, last_price)
            print("year_of_construction         :", new_year_of_construction, year_of_construction)
            print("exposition                   :", new_exposition, exposition)
            print("floor                        :", new_floor, floor)
            print("total_floor_number           :", new_total_floor_number, total_floor_number)
            print("neighborhood_descr     :", new_neighborhood_description, neighborhood_description)
            print("bedroom_number               :", new_bedroom_number, bedroom_number)
            print("toilet_number                :", new_toilet_number, toilet_number)
            print("bathroom_number              :", new_bathroom_number, bathroom_number)
            print("cellar                       :", new_cellar, cellar)
            print("lock_up_garage               :", new_lock_up_garage, lock_up_garage)
            print("heating                      :", new_heating, heating)
            print("tv_cable                     :", new_tv_cable, tv_cable)
            print("fireplace                    :", new_fireplace, fireplace)
            print("digicode                     :", new_digicode, digicode)
            print("intercom                     :", new_intercom, intercom)
            print("elevator                     :", new_elevator, elevator)
            print("fibre_optics_status          :", new_fibre_optics_status, fibre_optics_status)
            print("garden                       :", new_garden, garden)
            print("car_park_number              :", new_car_park_number, car_park_number)
            print("balcony                      :", new_balcony, balcony)
            print("large_balcony                :", new_large_balcony, large_balcony)
            print("dpe_date                     :", new_dpe_date, dpe_date)
            print("estate_agency_fee_% :", new_estate_agency_fee_percentage, estate_agency_fee_percentage)
            print("pinel                        :", new_pinel, pinel)
            print("denormandie                  :", new_denormandie, denormandie)
            print("announce_publication         :", new_announce_publication, announce_publication)
            print("announce_last_modif   :", new_announce_last_modification, announce_last_modification)
            print("ener_perf_letter :", new_energetic_performance_letter, energetic_performance_letter)
            print("ener_perf_number :", new_energetic_performance_number, energetic_performance_number)
            print("climatic_perf_number  :", new_climatic_performance_number, climatic_performance_number)
            print("climatic_perf_letter  :", new_climatic_performance_letter, climatic_performance_letter)
            if year_of_construction != new_year_of_construction:
                year_of_construction = new_year_of_construction
            if exposition != new_exposition:
                exposition = new_exposition
            if floor != new_floor:
                floor = new_floor

            if total_floor_number != new_total_floor_number:
                total_floor_number = new_total_floor_number
            if neighborhood_description != new_neighborhood_description:
                neighborhood_description = new_neighborhood_description

            # rooms
            if bedroom_number != new_bedroom_number:
                bedroom_number = new_bedroom_number
            if toilet_number != new_toilet_number:
                toilet_number = new_toilet_number
            if bathroom_number != new_bathroom_number:
                bathroom_number = new_bathroom_number
            if cellar != new_cellar:
                cellar = new_cellar
            if lock_up_garage != new_lock_up_garage:
                lock_up_garage = new_lock_up_garage

            # options indoor
            if heating != new_heating:
                heating = new_heating
            if tv_cable != new_tv_cable:
                tv_cable = new_tv_cable
            if fireplace != new_fireplace:
                fireplace = new_fireplace
            if digicode != new_digicode:
                digicode = new_digicode
            if intercom != new_intercom:
                intercom = new_intercom
            if elevator != new_elevator:
                elevator = new_elevator
            if fibre_optics_status != new_fibre_optics_status:
                fibre_optics_status = new_fibre_optics_status

            # options outdoor
            if garden != new_garden:
                garden = new_garden
            if car_park_number != new_car_park_number:
                car_park_number = new_car_park_number
            if balcony != new_balcony:
                balcony = new_balcony
            if large_balcony != new_large_balcony:
                large_balcony = new_large_balcony

            # administration
            if estate_agency_fee_percentage != new_estate_agency_fee_percentage:
                estate_agency_fee_percentage = new_estate_agency_fee_percentage
            if pinel != new_pinel:
                pinel = new_pinel
            if denormandie != new_denormandie:
                denormandie = new_denormandie
            if announce_publication != new_announce_publication:
                announce_publication = new_announce_publication
            if announce_last_modification != new_announce_last_modification:
                announce_last_modification = new_announce_last_modification

            # diagnostics
            if dpe_date != new_dpe_date:
                dpe_date = new_dpe_date
            if energetic_performance_letter != new_energetic_performance_letter:
                energetic_performance_letter = new_energetic_performance_letter
            if energetic_performance_number != new_energetic_performance_number:
                energetic_performance_number = new_energetic_performance_number
            if climatic_performance_number != new_climatic_performance_number:
                climatic_performance_number = new_climatic_performance_number
            if climatic_performance_letter != new_climatic_performance_letter:
                climatic_performance_letter = new_climatic_performance_letter

            print("----------------------Add new price Property---------------------")
            print(new_price)
            if last_price != new_price:
                database_app.add_price_to_property(new_date_add_to_db, id_property, new_price)
                print(f"{data.green}The price for property {id_property} has been update {new_price}{data.white}")
            else:
                print(f"{data.blue}No prices found for property {id_property}{data.white}")
            print("--------------------End add new price Property--------------------")
            print("----------------------Update Description---------------------")

            database_app.update_description(id_property,
                                            new_year_of_construction,
                                            new_exposition,
                                            new_floor,
                                            new_total_floor_number,
                                            new_neighborhood_description,
                                            new_bedroom_number,
                                            new_toilet_number,
                                            new_bathroom_number,
                                            new_cellar,
                                            new_lock_up_garage,
                                            new_heating,
                                            new_tv_cable,
                                            new_fireplace,
                                            new_digicode,
                                            new_intercom,
                                            new_elevator,
                                            new_fibre_optics_status,
                                            new_garden,
                                            new_car_park_number,
                                            new_balcony,
                                            new_large_balcony,
                                            new_estate_agency_fee_percentage,
                                            new_pinel, new_denormandie,
                                            new_announce_publication,
                                            new_announce_last_modification,
                                            new_dpe_date,
                                            new_energetic_performance_letter,
                                            new_energetic_performance_number,
                                            new_climatic_performance_number,
                                            new_climatic_performance_letter,
                                            estate_agency_id
                                            )
            announce_modified = True
            print("--------------------End Update Description------------------")

        if announce_modified:
            print("---------------------------------------END------------------------------------------")
            print(f"""{data.green}---------PROPERTY {id_property} HAS BEEN UPDATED---------{data.white}""")
            print("------------------------------------------------------------------------------------")
        else:
            print("---------------------------------------END------------------------------------------")
            print(f"""{data.blue}----------PROPERTY {id_property} HAS NOT BEEN UPDATED---------{data.white}""")
            print("------------------------------------------------------------------------------------")
