import logging
from copy import deepcopy

from ..constants import keys

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger('Preprocessing')

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