from selenium.webdriver.remote.webdriver import WebDriver

import logging

from geoid.config import Config
from geoid.constants import Keys, Status
from geoid.query import query


logger = logging.getLogger(__name__)


def get_iterator(
  queries_data: list[dict],
  webdriver: WebDriver,
  config: Config
):
  queries_count = len(queries_data)
  for index, data_object in enumerate(queries_data):
    logger.info(
      f'Query progress: ({index+1}/{queries_count})'
    )
    new_object, query_status = get_one(
      data_object, webdriver, config
    )
    
    yield new_object, index, query_status
  
  logger.info(
    'Reached end of query'
  )


def get_one(
  data_object: dict,
  webdriver: WebDriver,
  config: Config
):
  #: 1
  if data_object is None:
    return data_object, Status.QUERY_MISSING
  
  if Keys.QUERY_KEYWORD not in data_object:
    return data_object, Status.QUERY_MISSING
  
  if data_object[Keys.QUERY_KEYWORD] is None:
    return data_object, Status.QUERY_MISSING
  
  new_object = data_object.copy()
  query_keyword = data_object[Keys.QUERY_KEYWORD]

  if Keys.QUERY_STATUS not in new_object:
    new_object[Keys.QUERY_STATUS] = Status.QUERY_INCOMPLETE
    
  query_status = new_object[Keys.QUERY_STATUS]

  #: 2  
  if query_status == Status.QUERY_COMPLETE:
    return new_object, Status.QUERY_COMPLETE
  
  #: 3
  new_object.update(query.get(new_object, webdriver, use_config=config))

  #: 4
  query_status = new_object[Keys.QUERY_STATUS]
  if query_status == Status.QUERY_MISSING:
    logger.warning(
      f'Query object skipped due to missing query: {query_keyword}'
    )
  elif query_status == Status.QUERY_ERRORED:
    logger.error(
      f'Could not do query, continuing: {query_keyword}'
    )
  elif query_status == Status.QUERY_COMPLETE:
    logger.info(
      f'Completed query: {query_keyword}'
    )
  elif query_status == Status.QUERY_COMPLETE_MUNICIPALITIES_MISSING:
    logger.info(
      f'Completed query: {query_keyword}'
    )
    logger.warning(
      f'Query contains missing municipality data: {query_keyword}'
    )
  
  return new_object, query_status