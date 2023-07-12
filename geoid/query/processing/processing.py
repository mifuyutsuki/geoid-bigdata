from bs4 import Tag

from geoid.constants import Links, Keys
from . import fields

import requests


BASE_RESULT_ENTRY = {
  Keys.LOCATION_NAME : '',
  Keys.LOCATION_TYPE : '',
  Keys.LATITUDE      : '',
  Keys.LONGITUDE     : '',
  Keys.PROVINCE_ID   : '',
  Keys.PROVINCE_NAME : '',
  Keys.CITY_ID       : '',
  Keys.CITY_NAME     : '',
  Keys.DISTRICT_ID   : '',
  Keys.DISTRICT_NAME : '',
  Keys.VILLAGE_ID    : '',
  Keys.VILLAGE_NAME  : '',
  Keys.POSTAL_CODE   : '',
  Keys.RATING        : '',
  Keys.REVIEWS       : '',
  Keys.DESCRIPTION   : '',
  Keys.LOCATION_LINK : ''
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
  if (latitude == '' or longitude == ''):
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

  return result_entry


def _get_municipality_data(latitude: str, longitude: str) -> dict:
  request = requests.get(
    Links.MUNICIPALITY_QUERY_TARGET.format(
      latitude=str(latitude), longitude=str(longitude)
    ),
    timeout=(3.5, 5.0)
  )
  request.raise_for_status()
  response = request.json()
  return response