from bs4 import Tag

from geoid.constants import Links, Keys
from . import fields

import requests


BASE_RESULT_ENTRY = {
  Keys.LOCATION_NAME : None,
  Keys.LOCATION_TYPE : None,
  Keys.LATITUDE      : None,
  Keys.LONGITUDE     : None,
  Keys.PROVINCE_ID   : None,
  Keys.PROVINCE_NAME : None,
  Keys.CITY_ID       : None,
  Keys.CITY_NAME     : None,
  Keys.DISTRICT_ID   : None,
  Keys.DISTRICT_NAME : None,
  Keys.VILLAGE_ID    : None,
  Keys.VILLAGE_NAME  : None,
  Keys.POSTAL_CODE   : None,
  Keys.RATING        : None,
  Keys.REVIEWS       : None,
  Keys.DESCRIPTION   : None,
  Keys.LOCATION_LINK : None
}


def get_entry_fields(entry: Tag, query_lang='id') -> dict:
  #: 1. Fields initialization
  result_entry = BASE_RESULT_ENTRY.copy()

  #: 2. Fields get from HTML
  result_entry.update({
    Keys.LOCATION_NAME : fields.get_location_name(entry),
    Keys.LOCATION_TYPE : fields.get_location_type(entry),
    Keys.LATITUDE      : fields.get_latitude(entry) ,
    Keys.LONGITUDE     : fields.get_longitude(entry),
    Keys.RATING        : fields.get_rating(entry),
    Keys.REVIEWS       : fields.get_reviews(entry),
    Keys.DESCRIPTION   : fields.get_description(entry),
    Keys.LOCATION_LINK : fields.get_location_link(entry, query_lang)
  })
  
  return result_entry
  

def get_municipality_fields(result_entry: dict) -> dict:
  latitude  = result_entry[Keys.LATITUDE]
  longitude = result_entry[Keys.LONGITUDE]
  if (latitude is None or longitude is None):
    raise ValueError('Latitude/longitude field is empty')
  
  response = _get_municipality_data(latitude, longitude)
  
  new_result_entry = result_entry.copy()
  new_result_entry.update({
    Keys.PROVINCE_ID   : fields.get_province_id(response),
    Keys.PROVINCE_NAME : fields.get_province_name(response),
    Keys.CITY_ID       : fields.get_city_id(response),
    Keys.CITY_NAME     : fields.get_city_name(response),
    Keys.DISTRICT_ID   : fields.get_district_id(response),
    Keys.DISTRICT_NAME : fields.get_district_name(response),
    Keys.VILLAGE_ID    : fields.get_village_id(response),
    Keys.VILLAGE_NAME  : fields.get_village_name(response),
    Keys.POSTAL_CODE   : fields.get_postal_code(response)
  })

  return new_result_entry


def _get_municipality_data(latitude, longitude) -> dict:
  request = requests.get(
    Links.MUNICIPALITY_QUERY_TARGET.format(
      latitude=latitude, longitude=longitude
    ),
    timeout=(3.5, 5.0)
  )
  request.raise_for_status()
  response = request.json()
  return response