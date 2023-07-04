import logging
from copy import deepcopy

from geoid.constants import keys, status


logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def initialize(keyword: str, data: list[dict]) -> list[dict]:
  new_data = deepcopy(data)
  missings = 0

  for data_object in new_data:
    if keys.QUERY_TERM not in data_object:
      missings = missings + 1
      continue

    data_object = initialize_object(data_object)
    data_object[keys.QUERY] = f"{keyword} {data_object[keys.QUERY_TERM]}"
  
  if missings > 0:
    logger.warning(
      f'Found {str(missings)} entry(s) with missing query term, '
      f'which will be skipped'
    )

  return new_data


def initialize_object(data_object: dict) -> dict:
  new_object = data_object.copy()
  new_object[keys.QUERY]               = None
  new_object[keys.QUERY_LANG]          = ''
  new_object[keys.QUERY_TIMESTAMP]     = 0
  new_object[keys.QUERY_STATUS]        = status.QUERY_INCOMPLETE
  new_object[keys.QUERY_RESULTS_COUNT] = 0
  new_object[keys.QUERY_RESULTS]       = []
  return new_object
