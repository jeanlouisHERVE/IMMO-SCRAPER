#!/usr/bin/env python
# packages
import os

# other modules
from dotenv import load_dotenv

# own packages
import database_app
import update
import add_announces
import sql
import script_colors

database_app.create_tables()

# get data from .env file
load_dotenv()

# variables
city_researched_content = os.environ["CITY_RESEARCHED_CONTENT"]
menu_prompt = f"""-- Menu --

1) {script_colors.greenscript}Refresh database{script_colors.blackscript}
2) Run script to add description
3) Update descriptions
4) Update database architecture using sql
5) Number of announces
6) Exit

Enter your choice: """


def start_prompt():
    while True:
        user_input = input(menu_prompt)
        if user_input == "6":
            break  # exit the loop if user_input is "6"

        if user_input == "1":
            add_announces.add_new_announces()
        elif user_input == "2":
            add_announces.add_descriptions()
        elif user_input == "3":
            update.update_descriptions()
        elif user_input == "4":
            sql.sql()
            # add option to modify specific item based on id number
        elif user_input == "5":
            global_properties_number = database_app.get_properties_number()
            print(f"""\n--- The properties number --- \n\n
                  The city {city_researched_content} has a total of {global_properties_number[0][0]}
                  properties to sell. \n
                  """)
        else:
            print("Invalid input, please try again!")


# script
if __name__ == "__main__":
    start_prompt()
