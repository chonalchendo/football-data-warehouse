import pandas as pd
import requests
import pycountry
import pycountry_convert as pc
from bs4 import BeautifulSoup


def get_fifa_codes() -> dict[str, str]:
    """Returns a dictionary of FIFA country codes and country names.

    Returns:
        dict[str, str]: dictionary of FIFA country codes and country names
    """
    fifa_country_codes_url = "https://en.wikipedia.org/wiki/List_of_FIFA_country_codes"
    response = requests.get(fifa_country_codes_url)
    soup = BeautifulSoup(response.text, "html.parser")
    codes_table = soup.find_all("table", {"class": "wikitable"})
    df = pd.read_html(str(codes_table))
    fifa_codes = pd.concat(df[:4])
    return dict(zip(fifa_codes["Code"], fifa_codes["Country"]))


def get_continent_name(name: str) -> str:
    """Returns the continent of a country.

    Args:
        alpha3 (str): alpha3 code of country

    Returns:
        str: continent of country
    """
    match name:
        case name if isinstance(name, float):
            return "Unknown"
        case name if "congo" in name.lower():
            name = "congo"
        case name if "ivory" in name.lower():
            name = "Côte d'Ivoire"
        case name if "ireland" in name.lower():
            name = "ireland"
        case name if "verde" in name.lower():
            name = "verde"
        case name if "turkey" in name.lower():
            name = "turkiye"
        case name if "chinese taipei" in name.lower():
            name = "taiwan"
        case name if "east timor" in name.lower():
            return None
        case name if "macau" in name.lower():
            return None
        case name if "tahiti" in name.lower():
            return None
        case name if "u.s. virgin islands" in name.lower():
            return None

    alpha2 = pycountry.countries.search_fuzzy(name)[0].alpha_2
    continent_code = pc.country_alpha2_to_continent_code(alpha2)
    continent_name = pc.convert_continent_code_to_continent_name(continent_code)
    return continent_name
