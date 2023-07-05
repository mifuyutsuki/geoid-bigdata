import logging
from copy import deepcopy

from geoid.constants import Keys, status


logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def initialize(keyword: str, data: list[dict]) -> list[dict]:
  new_data = deepcopy(data)
  missings = 0

  for index, data_object in enumerate(new_data):
    if Keys.QUERY_TERM not in data_object:
      missings = missings + 1
      continue

    data_object = initialize_object(data_object)
    data_object[Keys.QUERY] = f"{keyword} {data_object[Keys.QUERY_TERM]}"
    new_data[index] = data_object
  
  if missings > 0:
    logger.warning(
      f'Found {str(missings)} entry(s) with missing query term, '
      f'which will be skipped'
    )

  return new_data


def initialize_object(data_object: dict) -> dict:
  new_object = data_object.copy()
  new_object[Keys.QUERY]               = None
  new_object[Keys.QUERY_LANG]          = ''
  new_object[Keys.QUERY_TIMESTAMP]     = 0
  new_object[Keys.QUERY_STATUS]        = status.QUERY_INCOMPLETE
  new_object[Keys.QUERY_RESULTS_COUNT] = 0
  new_object[Keys.QUERY_RESULTS]       = []
  return new_object
