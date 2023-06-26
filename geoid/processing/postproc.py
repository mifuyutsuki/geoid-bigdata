from unidecode import unidecode
from copy import deepcopy
import logging

from ..constants import keys

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger('Postprocessing')
  
def postproc_queries(
  data: list[dict]
) -> list[dict]:
  processed_data       = deepcopy(data)

  processed_data       = filter_by_city(processed_data)
  processed_data       = convert_flat(processed_data)
  processed_data       = convert_ascii(processed_data)
  processed_data       = replace_characters(processed_data, '\n', '; ')

  output_data          = processed_data
  objects_count_after  = len(output_data)

  logger.info(
    f'Outputted {str(objects_count_after)} entry(s)'
  )
  return output_data

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
  
  logger.debug(
    f'Flattened query results'
  )
  return flattened_data

def convert_ascii(data: list[dict]) -> list[dict]:
  ascii_data = data
  for query_result in ascii_data:
    for value in query_result.values():
      if type(value) is str:
        value = unidecode(value, errors='replace', replace_str='?')
  
  logger.debug(
    f'Converted all string fields to ASCII characters'
  )
  return ascii_data

def replace_characters(
  data: list[dict],
  char_from: str,
  char_to: str
) -> list[dict]:
  replaced_data = data
  for single_data in replaced_data:
    for value in single_data.values():
      if type(value) is str:
        value = value.replace(char_from, char_to)
  
  logger.debug(
    f'Converted all instances of "{char_from}" to "{char_to}"'
  )
  return replaced_data