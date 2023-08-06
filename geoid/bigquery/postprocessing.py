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

import unicodedata
import logging
from geoid.constants import Keys


logger = logging.getLogger(__name__)


def filter_by_city(data: list[dict]) -> list[dict]:
  filtered_data = data
  filtered_count = 0

  for data_object in filtered_data:
    try:
      target_city   = data_object[Keys.CITY_NAME]
      query_results = data_object[Keys.QUERY_RESULTS]
    except KeyError:
      #: Ignore missing-data objects
      continue
    
    filtered_query_results = []
    for query_result in query_results:
      query_city = query_result[Keys.CITY_NAME]
      if target_city.strip().lower() == query_city.strip().lower():
        filtered_query_results.append(query_result.copy())
      else:
        filtered_count = filtered_count + 1
      
    data_object[Keys.QUERY_RESULTS] = filtered_query_results
    data_object[Keys.QUERY_RESULTS_COUNT] = len(filtered_query_results)

  logger.info(
    f'Removed {str(filtered_count)} result(s) '
    f'with mismatched or missing location'
  )
  return filtered_data


def convert_flat(data: list[dict]) -> list[dict]:
  flattened_data = []

  for query_object in data:
    try:
      query_results = query_object[Keys.QUERY_RESULTS]
    except KeyError:
      continue
    
    head_object = dict()
    for key in query_object.keys():
      #: Include only some query keys
      if key in (
        Keys.QUERY_TERM, Keys.QUERY_LOCATION, Keys.QUERY_KEYWORD, \
        Keys.QUERY_LANG, Keys.QUERY_TIMESTAMP
      ):
        head_object[key] = query_object[key]

    for query_result in query_results:
      flattened_object = head_object.copy()
      flattened_object.update(query_result)
      flattened_data.append(flattened_object)
  
  flattened_data_count = len(flattened_data)
  logger.info(
    f'Flattened query results to {str(flattened_data_count)} entry(s)'
  )
  return flattened_data


def convert_ascii(data: list[dict]) -> list[dict]:
  ascii_data = data
  
  def fun(s):
    if isinstance(s, str):
      #: Looks a circular mess (encode -> decode), but it works.
      return str(
        unicodedata.normalize('NFKD', s)
                   .encode('ascii', 'replace')
                   .decode('utf-8', 'ignore')
      )
    else:
      return s
  ascii_data = lambda_values(ascii_data, fun)
  
  logger.info(
    f'Converted all string fields to ASCII characters'
  )
  return ascii_data


def replace_newline(data: list[dict]) -> list[dict]:
  return replace_characters(data, '\n', '; ')


def replace_characters(
  data: list[dict],
  char_from: str,
  char_to: str
) -> list[dict]:  
  replaced_data = data

  def fun(s):
    if isinstance(s, str):
      return s.replace(char_from, char_to)
    else:
      return s
  replaced_data = lambda_values(replaced_data, fun)

  logger.info(
    f'Converted all character instances of "{char_from}" to "{char_to}"'
  )
  return replaced_data


def lambda_values(
  data: list[dict],
  value_function
):
  target_data = data

  for single_data in target_data:
    for key in single_data.keys():
      if isinstance(single_data[key], list):
        target_data = lambda_values(single_data[key], value_function)
      elif isinstance(single_data[key], dict):
        pass
      else:
        single_data[key] = value_function(single_data[key])
  
  return target_data