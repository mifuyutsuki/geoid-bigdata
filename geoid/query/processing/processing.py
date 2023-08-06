# Copyright (c) 2023 Mifuyu (mifuyutsuki@proton.me)

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
from backoff import expo, on_exception

from geoid.constants import Links, Keys, Objects
from . import fields

import requests


def get_entry_fields(entry: Tag, query_lang='id') -> dict:
  #: 1. Fields initialization
  result_entry = Objects.BASE_PLACE_OBJECT.copy()

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


@on_exception(expo, requests.exceptions.RequestException, max_tries=5)
def _get_municipality_data(latitude, longitude) -> dict:
  request = requests.get(
    Links.MUNICIPALITY_QUERY_TARGET.format(
      latitude=latitude, longitude=longitude
    ),
    timeout=(2.5, 4.0)
  )
  request.raise_for_status()
  response = request.json()
  return response