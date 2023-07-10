from selenium.webdriver.remote.webdriver import WebDriver

import logging

from geoid.config import Config
from geoid.constants import Keys, Status
from geoid.query import query


logger = logging.getLogger(__name__)


def get_one(
  data_object: dict,
  webdriver: WebDriver,
  config: Config
):
  #: 1
  if data_object is None:
    return data_object, Status.QUERY_MISSING
  
  if Keys.QUERY not in data_object:
    return data_object, Status.QUERY_MISSING
  
  if data_object[Keys.QUERY] is None:
    return data_object, Status.QUERY_MISSING
  
  new_object = data_object.copy()

  if Keys.QUERY_STATUS not in new_object:
    new_object[Keys.QUERY_STATUS] = Status.QUERY_INCOMPLETE
    
  query_status = new_object[Keys.QUERY_STATUS]

  #: 2  
  if query_status == Status.QUERY_COMPLETE:
    return new_object, Status.QUERY_COMPLETE
  
  #: 3
  query_ = new_object[Keys.QUERY]
  results = query.get(query_, webdriver, use_config=config)
  new_object.update(results.report())
  
  return new_object, results.metadata.status