#packages
import os

#other modules
from dotenv import load_dotenv

#own packages
import modules.database_app
import modules.update
import modules.add_announces

modules.database_app.create_tables()
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
            modules.add_announces.add_new_announces()
        elif user_input == "2":
            modules.add_announces.add_descriptions()
        elif user_input == "3":
            modules.update.update_descriptions()
        elif user_input == "4":
            global_properties_number = modules.database_app.get_properties_number()
            print(f"""\n--- The properties number --- \n\n The city {city_researched_content} has a total of {global_properties_number[0][0]} properties to sell. \n 
                  """)
        else:
            print("Invalid input, please try again!")

#script
start_prompt()
