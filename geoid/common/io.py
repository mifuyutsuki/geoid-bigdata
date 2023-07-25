from geoid.constants import Keys, Objects
import os, json, logging


logger = logging.getLogger(__name__)


def import_data(filename: str):
  """
  Import a queries data JSON file.

  A warning is given when a query object contains missing required fields, most
  especially `query_keyword`.

  Args:
      filename (str): Filename of queries data JSON file
  
  Returns:
      Parsed queries data, which should be in the form of list of dicts (array
      of objects)
  """
  
  data = import_json(filename)

  locations = 0
  missings  = 0

  for data_object in data:
    if _is_keyword_missing(data_object):
      missings += 1
    else:
      locations += 1

  if missings > 0:
    logger.warning(
      f'Found {missings} entry(s) with missing query location, '
      f'which is skipped'
    )
  
  if locations == 0:
    logger.error(
      f'No locations to query'
    )
  else:
    logger.info(
      f'Locations to query: {locations}'
    )

  return data
  

def generate_data(term: str, cities: list[str]):
  """
  Generate a queries data from a list of cities.

  The output queries data can be readily used to launch a query, or may be
  customized if needed, for example to use a different query keyword than
  generated.

  Args:
      filename (str): Filename of queries data JSON file
  
  Returns:
      Queries data in the form of list of dicts (array of objects)
  """

  queries_data = []
  for city in cities:
    queries_data.append(_initialize_one(term, city))

  return queries_data


def generate_data_from_txt(term: str, filename: str):
  """
  Generate a queries data from a text file `filename`.

  The output queries data can be readily used to launch a query, or may be
  customized if needed, for example to use a different query keyword than
  generated.

  Args:
      filename (str): Filename of queries data JSON file
  
  Returns:
      Queries data in the form of list of dicts (array of objects)
  """

  cities = []
  with open(filename, 'r', encoding='UTF-8') as txt_file:
    for line in txt_file:
      if len(line) > 0:
        cities.append(line)

  return generate_data(term, cities)


def _initialize_one(term: str, location: str):
  query_object = Objects.BASE_QUERY_OBJECT.copy()
  query_object.update({
    Keys.QUERY_TERM     : term,
    Keys.QUERY_LOCATION : location,
    Keys.QUERY_KEYWORD  : f'{term} {location}'
  })
  return query_object


def _is_keyword_missing(query_object: dict):
  if query_object is None:
    return True
  if not isinstance(query_object.get(Keys.QUERY_KEYWORD), str):
    return True
  if len(query_object[Keys.QUERY_KEYWORD].strip()) <= 0:
    return True
  return False


def import_json(filename: str):
  with open(filename, 'r', encoding='UTF-8') as json_file:
    data = json.load(json_file)
  
  logger.info(
    f'Imported data from JSON file "{filename}"'
  )
  return data


def export_json(filename: str, data: list[dict], indent=1, **json_kwargs):
  with open(filename, 'w', encoding='UTF-8') as json_file:
    json.dump(data, json_file, indent=indent, **json_kwargs)
  
  logger.info(
    f'Exported data to JSON file "{filename}"'
  )


def remove_file(filename: str):
  try:
    os.remove(filename)
  except FileNotFoundError:
    logger.warning(
      f'No file to remove "{filename}"'
    )
    raise
  except OSError as e:
    logger.exception(e)
    logger.error(
      f'Could not remove file "{filename}"'
    )
  else:
    logger.info(
      f'Removed file "{filename}"'
    )