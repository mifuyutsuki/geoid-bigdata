from selenium.webdriver.remote.webdriver import WebDriver

from time import time
import logging

from . import scraping, parsing
from geoid.config import Config
from geoid.constants import Status, Keys


logger = logging.getLogger(__name__)


def get(
  query_object: dict,
  webdriver: WebDriver,
  use_config:Config=None
) -> dict:
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
  
  config = use_config if use_config else Config()

  new_query_object = query_object.copy()

  #: 0 - Checking
  if Keys.QUERY_KEYWORD not in new_query_object:
    return _update_status(new_query_object, Status.QUERY_MISSING)
  
  query = new_query_object[Keys.QUERY_KEYWORD]
  if len(query) <= 0:
    return _update_status(new_query_object, Status.QUERY_MISSING)

  #: Each try block represents a different process, which will output
  #: different line numbers in logs.

  #: 1 - Initializing
  query_status = new_query_object[Keys.QUERY_STATUS]

  query_lang = new_query_object[Keys.QUERY_LANG]
  if query_lang is None:
    query_lang = config.query.lang
  if len(query_lang) <= 0:
    query_lang = config.query.lang

  if query_status == Status.QUERY_COMPLETE or \
     query_status == Status.QUERY_COMPLETE_MUNICIPALITIES_MISSING:
    #: Go straight for municipality get
    results_list = new_query_object[Keys.QUERY_RESULTS]

  else:
    new_query_object.update({
      Keys.QUERY_LANG      : query_lang,
      Keys.QUERY_TIMESTAMP : int(time())
    })

  #: 2 - Scraping
    try:
      webdriver = scraping.get(query, webdriver, config, use_lang=query_lang)
      webdriver = scraping.scroll(webdriver, config)
    except Exception as e:
      logger.exception(e)
      return _update_status(new_query_object, Status.QUERY_ERRORED)
    
  #: 3 - Parsing
    try:
      results_html = scraping.grab(webdriver)
      results_list = parsing.parse_html(results_html, query_lang)
    except Exception as e:
      logger.exception(e)
      return _update_status(new_query_object, Status.QUERY_ERRORED)
  
  #: 4 - Municipality data
  try:
    results_list, municip_errors = parsing.get_municipality_data(results_list)
  except Exception as e:
    #: Note: Errors from acquiring individual municipality data are stored as
    #: error counts in municip_errors instead.
    logger.exception(e)
    return _update_status(new_query_object, Status.QUERY_ERRORED)
  
  #: 5 - Output
  new_query_object = _update_entries(new_query_object, results_list)
  
  if municip_errors > 0:
    return _update_status(new_query_object, Status.QUERY_COMPLETE_MUNICIPALITIES_MISSING)
  else:
    return _update_status(new_query_object, Status.QUERY_COMPLETE)


def _update_status(query_object: dict, query_status) -> dict:
  new_query_object = query_object.copy()
  new_query_object.update({
    Keys.QUERY_STATUS : query_status
  })
  return new_query_object


def _update_entries(query_object: dict, results: list[dict]) -> dict:
  new_query_object = query_object.copy()
  new_query_object.update({
    Keys.QUERY_RESULTS_COUNT : len(results),
    Keys.QUERY_RESULTS       : results
  })
  return new_query_object