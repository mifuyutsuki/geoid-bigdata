from bs4 import Tag

from ..constants import Keys
from . import fields

def proc_entry(entry: Tag, query_lang='id') -> dict:
    #: 1. Fields initialization
    result_entry = dict()
    result_entry[Keys.LOCATION_NAME] = fields.get_location_name(entry)
    result_entry[Keys.LOCATION_TYPE] = fields.get_location_type(entry)
    result_entry[Keys.LATITUDE]      = fields.get_latitude(entry) 
    result_entry[Keys.LONGITUDE]     = fields.get_longitude(entry)

    result_entry[Keys.PROVINCE_ID]   = ''
    result_entry[Keys.PROVINCE_NAME] = ''
    result_entry[Keys.CITY_ID]       = ''
    result_entry[Keys.CITY_NAME]     = ''
    result_entry[Keys.DISTRICT_ID]   = ''
    result_entry[Keys.DISTRICT_NAME] = ''
    result_entry[Keys.VILLAGE_ID]    = ''
    result_entry[Keys.VILLAGE_NAME]  = ''
    result_entry[Keys.POSTAL_CODE]   = ''

    result_entry[Keys.RATING]        = fields.get_rating(entry)
    result_entry[Keys.REVIEWS]       = fields.get_reviews(entry)
    result_entry[Keys.DESCRIPTION]   = fields.get_description(entry)
    result_entry[Keys.LOCATION_LINK] = fields.get_location_link(entry, query_lang)
    # result_entry[Keys.IMAGE_LINK]    = fields.get_image_link(entry)
    return result_entry
  
def proc_municipality(result_entry):
  if (
    result_entry[Keys.LATITUDE]  == '' or
    result_entry[Keys.LONGITUDE] == ''
  ):
    raise ValueError('Latitude/longitude field is empty')
  
  municipality_fields = fields.get_municipality_data(
      result_entry[Keys.LATITUDE],
      result_entry[Keys.LONGITUDE]
  )

  municipality_code = municipality_fields['code']

  province_id   = fields.get_province_id(municipality_code)
  province_name = str(municipality_fields['province'])
  city_id       = fields.get_city_id(municipality_code)
  city_name     = str(municipality_fields['city'])
  district_id   = fields.get_district_id(municipality_code)
  district_name = str(municipality_fields['district'])
  village_id    = fields.get_village_id(municipality_code)
  village_name  = str(municipality_fields['village'])
  postal_code   = str(municipality_fields['postal'])

  result_entry[Keys.PROVINCE_ID]   = province_id
  result_entry[Keys.PROVINCE_NAME] = province_name
  result_entry[Keys.CITY_ID]       = city_id
  result_entry[Keys.CITY_NAME]     = city_name
  result_entry[Keys.DISTRICT_ID]   = district_id
  result_entry[Keys.DISTRICT_NAME] = district_name
  result_entry[Keys.VILLAGE_ID]    = village_id
  result_entry[Keys.VILLAGE_NAME]  = village_name
  result_entry[Keys.POSTAL_CODE]   = postal_code

  return result_entry
