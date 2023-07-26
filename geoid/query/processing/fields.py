# Copyright (c) 2023 mifuyutsuki

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from bs4 import Tag
from urllib.parse import quote_plus
import re

from geoid.constants import Selectors


#: Municipality fields

def get_province_id(response: dict) -> int:
  subcodes = re.findall(r'[0-9]+', response['code'])
  return int(''.join(subcodes[0:1]))

def get_province_name(response: dict) -> str:
  return response['province']

def get_city_id(response: dict) -> str:
  subcodes = re.findall(r'[0-9]+', response['code'])
  return int(''.join(subcodes[0:2]))

def get_city_name(response: dict) -> str:
  return response['city']

def get_district_id(response: dict) -> int:
  subcodes = re.findall(r'[0-9]+', response['code'])
  return int(''.join(subcodes[0:3]))

def get_district_name(response: dict) -> str:
  return response['district']

def get_village_id(response: dict) -> int:
  subcodes = re.findall(r'[0-9]+', response['code'])
  return int(''.join(subcodes))

def get_village_name(response: dict) -> str:
  return response['village']

def get_postal_code(response: dict) -> int:
  return response['postal']


#: Entry fields

def get_location_name(entry: Tag) -> str:
  field_selection = entry.select_one(Selectors.LOCATION_NAME_FIELD)

  if field_selection is not None:
    field = field_selection.string
  else:
    field = ''
  return field

def get_location_type(entry: Tag) -> str:
  field_selection = entry.select_one(Selectors.LOCATION_TYPE_FIELD)

  if field_selection is not None:
    field = field_selection.string
  else:
    field = ''
  return field
    
def get_latitude(entry: Tag) -> float:
  field_selection = entry.select_one(Selectors.LATITUDE_FIELD)
  field = field_selection['href']
  field_regex = re.search(r'(?<=!3d)-?[0-9]+[.,].[0-9]+', field)
  return float(field_regex.group(0))
    
def get_longitude(entry: Tag) -> float:
  field_selection = entry.select_one(Selectors.LONGITUDE_FIELD)
  field = field_selection['href']
  field_regex = re.search(r'(?<=!4d)-?[0-9]+[.,].[0-9]+', field)
  return float(field_regex.group(0))

def get_rating(entry: Tag) -> float:
  # Rating is of the form 4.8 or 4,8
  # -> Account for decimal comma
  field_selection = entry.select_one(Selectors.RATING_FIELD)

  if field_selection is None:
    return 0.0
  else:
    field = field_selection.string.replace(',', '.')
    return float(field)

def get_reviews(entry: Tag) -> int:
  # Review count is of the form (11,111) or (11.111)
  # -> Ignore non-numbers
  field_selection = entry.select_one(Selectors.REVIEWS_FIELD)

  if field_selection is None:
    return 0
  else:
    field = field_selection.string
    field = re.sub('[^0-9]', '', field)
    return int(field)

def get_description(entry: Tag) -> str:
  #: Description is of the form [" ", " ", " ", " "]
  #: -> Join same-line blocks with whitespace
  #: -> Join different lines with newline
  field_selections = entry.select(Selectors.DESCRIPTION_FIELD)

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
  field_selection = entry.select_one(Selectors.LOCATION_LINK_FIELD)

  if field_selection is not None:
    field = field_selection['href'].rsplit('?')[0] + f'?hl={quote_plus(query_lang)}'
  else:
    field = ''
  return field

# Unused
def get_image_link(entry: Tag) -> str:
  #: Stripping the section after '=' yields the original size img
  field_selection = entry.select_one(Selectors.IMAGE_LINK_FIELD)

  if field_selection is not None:
    field = field_selection['src'].rsplit('=')[0]
  else:
    field = ''
  return field