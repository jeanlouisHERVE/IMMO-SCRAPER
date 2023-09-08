#packages
import os

#other modules
from dotenv import load_dotenv

#own packages
import database
import update
import add_announces

database.create_tables()
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

###TODO add a price table with history
###TODO send old announces to another table
###TODO migration to another base of unpublished announces