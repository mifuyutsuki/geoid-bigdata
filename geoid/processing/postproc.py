from unidecode import unidecode
from copy import deepcopy
import logging

from ..constants import keys

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger('Postprocessing')

def filter_by_city(data: list[dict]) -> list[dict]:
  filtered_data = data
  filtered_count = 0

  for data_object in filtered_data:
    try:
      target_city   = data_object[keys.CITY_NAME]
      query_results = data_object[keys.QUERY_RESULTS]
    except KeyError:
      continue
    
    filtered_query_results = []
    for query_result in query_results:
      query_city = query_result[keys.CITY_NAME]
      if (
        target_city.strip().lower() == query_city.strip().lower()
      ):
        filtered_query_results.append(query_result.copy())
      else:
        filtered_count = filtered_count + 1
      
    data_object[keys.QUERY_RESULTS] = filtered_query_results
    data_object[keys.QUERY_RESULTS_COUNT] = len(filtered_query_results)

  logger.info(
    f'Removed {str(filtered_count)} result(s) '
    f'with mismatched or missing location'
  )
  return filtered_data

def convert_flat(data: list[dict]) -> list[dict]:
  flattened_data = []

  for query_object in data:
    try:
      query_results = query_object[keys.QUERY_RESULTS]
    except KeyError:
      continue
    
    head_object = dict()
    for key in query_object.keys():
      #: Whitelist only query information keys
      if key in (
        keys.QUERY_TERM, keys.QUERY, keys.QUERY_LANG, keys.QUERY_TIMESTAMP
      ):
        head_object[key] = query_object[key]

    for query_result in query_results:
      flattened_object = head_object.copy()
      flattened_object.update(query_result)
      flattened_data.append(flattened_object)
  
  flattened_data_count = len(flattened_data)
  logger.debug(
    f'Flattened query results to {str(flattened_data_count)} entry(s)'
  )
  return flattened_data

def convert_ascii(data: list[dict]) -> list[dict]:
  ascii_data = data
  
  def fun(s):
    if isinstance(s, str):
      return unidecode(s, errors='replace', replace_str='?')
    else:
      return s
  ascii_data = lambda_values(ascii_data, fun)
  
  logger.debug(
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

  logger.debug(
    f'Converted all instances of "{char_from}" to "{char_to}"'
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
        target_data = lambda_values(target_data, value_function)
      elif isinstance(single_data[key], dict):
        pass
      else:
        single_data[key] = value_function(single_data[key])
  
  return target_data