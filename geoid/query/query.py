from selenium.webdriver.remote.webdriver import WebDriver

from time import time
import logging

from . import scraping, parsing
from .results import Results
from geoid.config import Config
from geoid.constants import status

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

def get(
  query: str,
  webdriver: WebDriver,
  use_config:Config=None
):
  if len(query) <= 0:
    raise ValueError('Query key must not be empty')
  
  config = use_config if use_config else Config()
  
  results = Results()
  results.metadata.status    = status.QUERY_INCOMPLETE
  results.metadata.query     = query
  results.metadata.lang      = config.query.lang
  results.metadata.timestamp = int(time())

  try:
  #: 1
    webdriver = scraping.get(query, webdriver, config)

  #: 2
    webdriver = scraping.scroll(webdriver, config)
  
  except Exception as e:
    logger.error(str(e))
    results.metadata.status = status.QUERY_ERRORED
    return results
  
  #: 3
  results_html = scraping.grab(webdriver)
  
  #: 4
  results_list = parsing.parse_html(results_html, results.metadata)

  #: 5
  results_list = parsing.get_municipality_data(results_list)

  results.results         = results_list
  results.count           = len(results_list)
  results.metadata.status = status.QUERY_COMPLETE
  return results