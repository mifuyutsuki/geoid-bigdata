import logging
from copy import deepcopy

from geoid.constants import Keys, Status


logger = logging.getLogger(__name__)


def initialize(keyword: str, data: list[dict]) -> list[dict]:
  new_data = deepcopy(data)
  missings = 0

  for index, data_object in enumerate(new_data):
    #: Do this first for dict ordering reasons
    if Keys.QUERY_LOCATION not in data_object:
      missings = missings + 1
      data_object[Keys.QUERY_LOCATION] = None
    
    data_object = initialize_object(data_object)

    if data_object[Keys.QUERY_LOCATION] is not None:
      data_object[Keys.QUERY_KEYWORD] = f"{keyword} {data_object[Keys.QUERY_LOCATION]}"

    #: Using index assignment as otherwise new_data would not be modified
    new_data[index] = data_object
  
  if missings > 0:
    logger.warning(
      f'Found {str(missings)} entry(s) with missing query term, '
      f'which will be skipped'
    )

  return new_data


def initialize_object(data_object: dict) -> dict:
  new_object = data_object.copy()
  new_object[Keys.QUERY_KEYWORD]               = None
  new_object[Keys.QUERY_LANG]          = ''
  new_object[Keys.QUERY_TIMESTAMP]     = 0
  new_object[Keys.QUERY_STATUS]        = Status.QUERY_INCOMPLETE
  new_object[Keys.QUERY_RESULTS_COUNT] = 0
  new_object[Keys.QUERY_RESULTS]       = []
  return new_object


def report_object(data_object: dict):
  query_status = Status.QUERY_INCOMPLETE

  if data_object is None:
    query_status = Status.QUERY_MISSING

  if Keys.QUERY_STATUS not in data_object:
    query_status = Status.QUERY_MISSING

  query_status = data_object[Keys.QUERY_STATUS]

  return query_status