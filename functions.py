import pytz
import datetime


def date_converter_french_to_english(french_date):
    
    months = {
    "janvier":"january",
    "fevrier":"february",
    "mars":"march",
    "avril":"april",
    "mai":"may",
    "juin":"june",
    "juillet":"july",
    "août":"augustus",
    "septembre":"september",
    "octobre":"october",
    "novembre":"november",
    "décembre":"december"
    }  

    date_parts = french_date.split()
    french_month = date_parts[1].lower()
    
    try:
        en_month = months[french_month]
        english_month = months.get(date_parts[1].lower(), date_parts[1])
        formatted_date = f"{date_parts[0]} {english_month} {date_parts[2]}"
        print("formatted_date",formatted_date)
        dt_object = datetime.datetime.strptime(formatted_date, "%d %B %Y")
        utc_timestamp = dt_object.replace(tzinfo=pytz.UTC).timestamp()
        return utc_timestamp
        
    except KeyError:
        print(f"KO : The provided french month '{french_month}' does not exists")
        return None
    
    
    
    
    
    