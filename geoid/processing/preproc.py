import logging
from copy import deepcopy

from geoid.constants import Keys


logger = logging.getLogger('Preprocessing')


def preproc_queries(
  keyword: str,
  data: list[dict]
) -> list[dict]:
  output_data = deepcopy(data)

  for data_object in output_data:
    try:
      data_object[Keys.QUERY_TERM]
    except KeyError:
      continue

    data_object[Keys.QUERY] = f"{keyword} {data_object[Keys.QUERY_TERM]}"
  
  return output_data