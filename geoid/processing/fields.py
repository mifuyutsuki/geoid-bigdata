from bs4 import Tag
from urllib.parse import quote_plus
import requests
import re

from ..constants import cselectors, links

def get_municipality_data(latitude, longitude):
  request = requests.get(
    links.MUNICIPALITY_QUERY_TARGET.format(
      latitude=str(latitude), longitude=str(longitude)
    ),
    timeout=(3.5, 5.0)
  )
  request.raise_for_status()
  return request.json()

def get_province_id(code) -> str:
  subcodes = re.findall(r'[0-9]+', code)
  try:
    field  = ''.join(subcodes[0:1])
  except IndexError:
    field  = ''
  return field

def get_city_id(code) -> str:
  subcodes = re.findall(r'[0-9]+', code)
  try:
    field  = ''.join(subcodes[0:2])
  except IndexError:
    field  = ''
  return field

def get_district_id(code) -> str:
  subcodes = re.findall(r'[0-9]+', code)
  try:
    field  = ''.join(subcodes[0:3])
  except IndexError:
    field  = ''
  return field

def get_village_id(code) -> str:
  subcodes = re.findall(r'[0-9]+', code)
  try:
    field  = ''.join(subcodes)
  except IndexError:
    field  = ''
  return field

def get_location_name(entry: Tag) -> str:
  field_selection = entry.select_one(cselectors.LOCATION_NAME_FIELD)

  if field_selection is not None:
    field = field_selection.string
  else:
    field = ''
  return field

def get_location_type(entry: Tag) -> str:
  field_selection = entry.select_one(cselectors.LOCATION_TYPE_FIELD)

  if field_selection is not None:
    field = field_selection.string
  else:
    field = ''
  return field
    
def get_latitude(entry: Tag) -> str:
  field_selection = entry.select_one(cselectors.LATITUDE_FIELD)

  if field_selection is not None:
    field = field_selection['href']
  else:
    field = ''
  
  field_regex = re.search(r'(?<=!3d)-?[0-9]+[.,].[0-9]+', field)
  if field_regex is not None:
    field = field_regex.group(0)
  return field
    
def get_longitude(entry: Tag) -> str:
  field_selection = entry.select_one(cselectors.LONGITUDE_FIELD)

  if field_selection is not None:
    field = field_selection['href']
  else:
    field = ''
  
  field_regex = re.search(r'(?<=!4d)-?[0-9]+[.,].[0-9]+', field)
  if field_regex is not None:
    field = field_regex.group(0)
  return field

def get_rating(entry: Tag) -> str:
  # Rating is of the form 4.8 or 4,8
  # -> Account for decimal comma
  field_selection = entry.select_one(cselectors.RATING_FIELD)

  if field_selection is not None:
    field = field_selection.string
    field = field.replace(',', '.')
  else:
    field = ''
  return field

def get_reviews(entry: Tag) -> str:
  # Review count is of the form (11,111) or (11.111)
  # -> Ignore non-numbers
  field_selection = entry.select_one(cselectors.REVIEWS_FIELD)

  if field_selection is not None:
    field = field_selection.string
    field = re.sub('[^0-9]', '', field)
  else:
    field = ''
  return field

def get_description(entry: Tag) -> str:
  #: Description is of the form [" ", " ", " ", " "]
  #: -> Join same-line blocks with whitespace
  #: -> Join different lines with newline
  field_selections = entry.select(cselectors.DESCRIPTION_FIELD)

  field_lines = []
  for index, selection in enumerate(field_selections):
    #: Skip the first field, as it is already processed as location type 
    if index == 0:
      continue
    field_lines.append(' '.join(list(selection.stripped_strings)))
  field = '\n'.join(field_lines)
  return field

def get_location_link(entry: Tag, query_lang: str) -> str:
  #: The section after '?' grabbed from the fields can be dropped
  #: However, keep the host query_lang query (from caller)
  field_selection = entry.select_one(cselectors.LOCATION_LINK_FIELD)

  if field_selection is not None:
    field = field_selection['href'].rsplit('?')[0] + f'?hl={quote_plus(query_lang)}'
  else:
    field = ''
  return field

def get_image_link(entry: Tag) -> str:
  #: Stripping the section after '=' yields the original size img
  field_selection = entry.select_one(cselectors.IMAGE_LINK_FIELD)

  if field_selection is not None:
    field = field_selection['src'].rsplit('=')[0]
  else:
    field = ''
  return field