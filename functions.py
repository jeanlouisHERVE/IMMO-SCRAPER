


def month_converter(month):
    
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
     
    try:
        en_month = months[month]
        return en_month
    except KeyError:
        print(f"KO : The provided month '{month}' does not exists")
        return None