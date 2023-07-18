import logging
from geoid.constants import Keys, Status


logger = logging.getLogger(__name__)

BASE_DATA_OBJECT = {
  Keys.QUERY_TERM          : None,
  Keys.QUERY_LOCATION      : None,
  Keys.QUERY_KEYWORD       : None,
  Keys.QUERY_LANG          : None,
  Keys.QUERY_TIMESTAMP     : 0,
  Keys.QUERY_STATUS        : Status.QUERY_INCOMPLETE,
  Keys.QUERY_RESULTS_COUNT : 0,
  Keys.QUERY_RESULTS       : []
}


def initialize_from_save(data: list[dict]):
  locations_count = 0
  missings_count  = 0

  for data_object in data:
    if data_object is None:
      missings_count += 1
      continue
    if Keys.QUERY_KEYWORD not in data_object:
      missings_count += 1
      continue
    if len(data_object[Keys.QUERY_KEYWORD]) <= 0:
      missings_count += 1
      continue
    locations_count += 1
  
  _log_counts(locations_count, missings_count)
  
  return data


def initialize_from_data(term: str, data: list[dict]) -> list[dict]:
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

  queries_data    = []
  locations_count = 0
  missings_count  = 0

  for data_object in data:
    query_object = _initialize_one_from_data(term, data_object)
    if query_object is None:
      missings_count += 1
    else:
      locations_count += 1
      queries_data.append(query_object)
  
  _log_counts(locations_count, missings_count)

  return queries_data


def initialize_from_list(term: str, locations: list[str]) -> list[dict]:
  """
  Generate a queries data from a list (array) of citynames in `locations`.

  For all non-empty citynames in `locations`, generate a base queries data
  containing queries of "`term` `cityname`" for all citynames in `locations`.

  Args:
      term (str): Query term to which will be appended with citynames.
      locations (list[str]): Array of locations or citynames.
  
  Returns:
      List of dicts (array of objects) containing base query information.
  """

  queries_data    = []
  locations_count = 0
  missings_count  = 0

  for location in locations:
    query_object = _initialize_one(term, location)
    if query_object is None:
      missings_count += 1
    else:
      locations_count += 1
      queries_data.append(query_object)
  
  _log_counts(locations_count, missings_count)

  return queries_data


def _initialize_one_from_data(term: str, data_object: dict) -> dict | None:
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

  location = _get_location_from_data(data_object)
  if location is None:
    return None

  return _initialize_one(term, location)


def _initialize_one(term: str, location: str):
  if location is None:
    return None
  if len(location) <= 0:
    return None

  query_object = BASE_DATA_OBJECT.copy()
  query_object.update({
    Keys.QUERY_TERM     : term,
    Keys.QUERY_LOCATION : location,
    Keys.QUERY_KEYWORD  : f'{term} {location}'
  })
  return query_object


def _get_location_from_data(data_object: dict):
  if Keys.QUERY_LOCATION not in data_object:
    return None
  
  location = data_object[Keys.QUERY_LOCATION]
  if location is None:
    return None
  if len(location) <= 0:
    return None

  return location


def _log_counts(locations: int, missings: int):
  if missings > 0:
    logger.warning(
      f'Found {missings} entry(s) with missing query location, '
      f'which is skipped'
    )
  
  if locations == 0:
    logger.warning(
      f'No locations to query'
    )
  else:
    logger.info(
      f'Locations to query: {locations}'
    )