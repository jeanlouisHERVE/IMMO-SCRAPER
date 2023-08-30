import re
import pytz
import datetime


def date_converter_french_date_to_utc_timestamp(french_date):
    
    months = {
    "janvier":"01",
    "fevrier":"02",
    "mars":"03",
    "avril":"04",
    "mai":"05",
    "juin":"06",
    "juillet":"07",
    "août":"08",
    "septembre":"09",
    "octobre":"10",
    "novembre":"11",
    "décembre":"12"
    }  

    regex_number = r'\d+'
    
    date_parts = french_date.split()
    french_month = date_parts[1].lower()
    
    ###extract numbers in day part
    day_number = re.findall(regex_number, date_parts[0])[0]
    
    try:
        check_month = months[french_month]
        number_month = months.get(date_parts[1].lower(), date_parts[1])
        formatted_date = f"{day_number}-{number_month}-{date_parts[2]}"
        print("formatted_date",formatted_date)
        dt_object = datetime.datetime.strptime(formatted_date, "%d-%m-%Y")
        utc_timestamp = dt_object.replace(tzinfo=pytz.UTC).timestamp()
        return utc_timestamp
        
    except KeyError:
        print(f"KO : The provided french month '{french_month}' does not exists")
        return None
    
    
    
    
    
    