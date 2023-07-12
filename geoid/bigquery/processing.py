import unidecode
import logging
from geoid.constants import Keys, Status


logger = logging.getLogger(__name__)

BASE_DATA_OBJECT = {
  Keys.QUERY_LOCATION      : None,
  Keys.QUERY_KEYWORD       : None,
  Keys.QUERY_LANG          : None,
  Keys.QUERY_TIMESTAMP     : 0,
  Keys.QUERY_STATUS        : Status.QUERY_INCOMPLETE,
  Keys.QUERY_RESULTS_COUNT : 0,
  Keys.QUERY_RESULTS       : []
}


def initialize(term: str, data: list[dict]) -> list[dict]:
  """
  Generate a queries data from an imported list of citynames in `data`.

  For all non-missing citynames given by each object in `data`, generate a base
  queries data containing queries of "`term` `cityname`" for all citynames in
  `data`.

  Args:
      term (str): Query term to which will be appended with citynames.
      data (list[dict]): Array of objects containing citynames.
  
  Returns:
      List of dicts (array of objects) containing base query information.
  """

  queries_data     = []
  locations_count  = 0
  missings_count   = 0

  for data_object in data:
    query_object = _initialize_one(term, data_object)
    if query_object is None:
      missings_count += 1
    else:
      locations_count += 1
      queries_data.append(query_object)
  
  if missings_count > 0:
    logger.warning(
      f'Found {missings_count} entry(s) with missing query location, '
      f'which is skipped'
    )

  return queries_data


def _initialize_one(term: str, data_object: dict) -> dict | None:
  """
  Generate a single query object from a cityname in `data_object`.

  Generate a query object for query "`term` `cityname`" using cityname provided
  by `data_object`. Cityname is given by a field of key `Keys.QUERY_LOCATION`.
  If the requisite key is missing, this function returns None.

  Args:
      term (str): Query term which will be appended with cityname.
      data_object (dict): Data object which contains cityname.
  Returns:
      Dict (object) containing base query information.
      None if field of key `Keys.QUERY_LOCATION` from `data_object` is missing
      or empty.
  """

  if Keys.QUERY_LOCATION not in data_object:
    return None
  
  location = data_object[Keys.QUERY_LOCATION]
  if location is None:
    return None
  if len(location) <= 0:
    return None

  query_object = BASE_DATA_OBJECT.copy()
  query_object.update({
    Keys.QUERY_LOCATION : location,
    Keys.QUERY_KEYWORD  : f'{term} {location}'
  })
  return query_object


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
      #: Whitelist only query information keys
      if key in (
        Keys.QUERY_LOCATION, Keys.QUERY_KEYWORD, Keys.QUERY_LANG, Keys.QUERY_TIMESTAMP
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
      return unidecode(s, errors='replace', replace_str='?')
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
        target_data = lambda_values(target_data, value_function)
      elif isinstance(single_data[key], dict):
        pass
      else:
        single_data[key] = value_function(single_data[key])
  
  return target_data