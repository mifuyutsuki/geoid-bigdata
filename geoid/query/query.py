from selenium.webdriver.remote.webdriver import WebDriver

from time import time
import logging

from . import scraping, parsing
from .results import Results
from geoid.config import Config
from geoid.constants import Status, Keys


logger = logging.getLogger(__name__)


def get(
  query: str,
  webdriver: WebDriver,
  use_config:Config=None
):
  """
  Search GMaps for `query` and return results of places.

  Return a Results object containing query results for term `query` and query
  information such as its timestamp (logged on query start). Uses Selenium
  web client given by `webdriver`.

  Status of results are given by the value of `results.metadata.status`
  corresponding to values in `geoid.constants.Status`. Errors during querying
  are signalled through the metadata variable's value.

  Args:
      query (str): Search or query keyword.
      webdriver (WebDriver): Selenium web-client/webdriver object.
      use_config (Config): Config object containing advanced query and program
      settings.
  
  Returns:
      Results object containing query information and results.
  """

  if len(query) <= 0:
    raise ValueError('Query key must not be empty')
  
  config = use_config if use_config else Config()
  
  results = Results()
  results.metadata.status    = Status.QUERY_INCOMPLETE
  results.metadata.query     = query
  results.metadata.lang      = config.query.lang
  results.metadata.timestamp = int(time())

  #: Each try block represents a different process, which will output
  #: different line numbers in logs.

  try:
  #: 1 - Scraping
    webdriver = scraping.get(query, webdriver, config)
    webdriver = scraping.scroll(webdriver, config)
  except Exception as e:
    logger.error(str(e))
    results.metadata.status = Status.QUERY_ERRORED
    return results
  
  try:
  #: 2 - Parsing
    results_html = scraping.grab(webdriver)
    results_list = parsing.parse_html(results_html, results.metadata)
  except Exception as e:
    logger.error(str(e))
    results.metadata.status = Status.QUERY_ERRORED
    return results

  try:
  #: 3 - Municipality data
    results_list, municip_errors = parsing.get_municipality_data(results_list)
  except Exception as e:
    #: Note: Errors from acquiring individual municipality data are stored as
    #: error counts in municip_errors instead.
    logger.error(str(e))
    results.metadata.status = Status.QUERY_ERRORED
    return results
  
  #: 4 - Output
  results.results         = results_list
  results.count           = len(results_list)
  if municip_errors > 0:
    results.metadata.status = Status.QUERY_COMPLETE_MUNICIPALITIES_MISSING
  else:
    results.metadata.status = Status.QUERY_COMPLETE

  return results


def get_saved(data_object: dict):
  """
  Get a Results object from a dict.

  Use to load one query object from an autosave or an unpostprocessed export.

  Args:
      data_object (dict): Query object dictionary containing query information
      and results.
  
  Returns:
      Results object containing query information and results.
  """

  results = Results()
  results.metadata.status    = data_object[Keys.QUERY_STATUS]
  results.metadata.query     = data_object[Keys.QUERY_KEYWORD]
  results.metadata.lang      = data_object[Keys.QUERY_LANG]
  results.metadata.timestamp = data_object[Keys.QUERY_TIMESTAMP]
  results.results            = data_object[Keys.QUERY_RESULTS]
  results.count              = data_object[Keys.QUERY_RESULTS_COUNT]

  return results