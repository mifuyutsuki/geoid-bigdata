import logging
from copy import deepcopy

from ..constants import keys

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger('Processing')

def preproc_queries(
  keyword: str,
  data: list[dict]
) -> list[dict]:
  output_data = deepcopy(data)

  for data_object in output_data:
    try:
      data_object[keys.QUERY_TERM]
    except KeyError:
      continue

    data_object[keys.QUERY] = f"{keyword} {data_object[keys.QUERY_TERM]}"
  
  return output_data
  
def postproc_queries(
  data: list[dict]
) -> list[dict]:
  unprocessed_data    = deepcopy(data)

  filtered_data       = _postproc_filter(unprocessed_data)
  flattened_data      = _postproc_flatten(filtered_data)

  output_data         = flattened_data
  objects_count_after = len(output_data)

  logger.info(
    f'Postprocessing outputted {str(objects_count_after)} entry(s)'
  )
  return output_data

def _postproc_filter(
  data: list[dict]
) -> list[dict]:
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
    f'Postprocessing - removed {str(filtered_count)} result(s) '
    f'with mismatched or missing location'
  )
  return filtered_data

def _postproc_flatten(
  data: list[dict]
) -> list[dict]:
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
  
  logger.info(
    f'Postprocessing - flattened query results'
  )
  return flattened_data