from bs4 import Tag

from ..constants import keys
from . import fields

def proc_entry(entry: Tag, query_lang='id') -> dict:
    #: 1. Fields initialization
    result_entry = dict()
    result_entry[keys.LOCATION_NAME] = fields.get_location_name(entry)
    result_entry[keys.LOCATION_TYPE] = fields.get_location_type(entry)
    result_entry[keys.LATITUDE]      = fields.get_latitude(entry) 
    result_entry[keys.LONGITUDE]     = fields.get_longitude(entry)

    result_entry[keys.PROVINCE_ID]   = ''
    result_entry[keys.PROVINCE_NAME] = ''
    result_entry[keys.CITY_ID]       = ''
    result_entry[keys.CITY_NAME]     = ''
    result_entry[keys.DISTRICT_ID]   = ''
    result_entry[keys.DISTRICT_NAME] = ''
    result_entry[keys.VILLAGE_ID]    = ''
    result_entry[keys.VILLAGE_NAME]  = ''
    result_entry[keys.POSTAL_CODE]   = ''

    result_entry[keys.RATING]        = fields.get_rating(entry)
    result_entry[keys.REVIEWS]       = fields.get_reviews(entry)
    result_entry[keys.DESCRIPTION]   = fields.get_description(entry)
    result_entry[keys.LOCATION_LINK] = fields.get_location_link(entry, query_lang)
    result_entry[keys.IMAGE_LINK]    = fields.get_image_link(entry)
    return result_entry
  
def proc_municipality(result_entry):
  if (
    result_entry[keys.LATITUDE]  == '' or
    result_entry[keys.LONGITUDE] == ''
  ):
    raise ValueError('Latitude/longitude field is empty')
  
  municipality_fields = fields.get_municipality_data(
      result_entry[keys.LATITUDE],
      result_entry[keys.LONGITUDE]
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

  result_entry[keys.PROVINCE_ID]   = province_id
  result_entry[keys.PROVINCE_NAME] = province_name
  result_entry[keys.CITY_ID]       = city_id
  result_entry[keys.CITY_NAME]     = city_name
  result_entry[keys.DISTRICT_ID]   = district_id
  result_entry[keys.DISTRICT_NAME] = district_name
  result_entry[keys.VILLAGE_ID]    = village_id
  result_entry[keys.VILLAGE_NAME]  = village_name
  result_entry[keys.POSTAL_CODE]   = postal_code

  return result_entry
