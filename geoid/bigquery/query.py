from selenium.webdriver.remote.webdriver import WebDriver

import logging

from geoid.common import io
from geoid.config import Config
from geoid.constants import Keys, Status
from geoid.query import query
from . import processing


logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def import_cities(
  source_filename: str,
  keyword: str
):
  data = io.import_json(source_filename)
  data = processing.initialize(keyword, data)
  #: verify?

  return data


def get_one(
  data_object: dict,
  webdriver: WebDriver,
  config: Config
):
  new_object = data_object.copy()

  #: 1
  if new_object is None:
    return new_object, Status.QUERY_MISSING
  
  if Keys.QUERY not in new_object:
    return new_object, Status.QUERY_MISSING

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