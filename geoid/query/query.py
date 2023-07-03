from selenium.webdriver.remote.webdriver import WebDriver

from time import time
import logging

from . import scraping, parsing
from .results import Results
from geoid.config import Config

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
  results.metadata.status    = results.metadata.STATUS_INCOMPLETE
  results.metadata.query     = query
  results.metadata.lang      = config.query.lang
  results.metadata.timestamp = int(time())

  try:
  #: 1
    logger.info(
      f'Starting query: "{query}"'
    )
    webdriver = scraping.get(query, webdriver, config)

  #: 2
    logger.info(
      f'Scrolling query: "{query}"'
    )
    webdriver = scraping.scroll(webdriver, config)
  
  except Exception as e:
    logger.error(str(e))
    results.metadata.status = results.metadata.STATUS_ERRORED
    return results
  
  #: 3
  results_html = scraping.grab(webdriver)
  
  #: 4
  logger.info(
    f'Processing results of query: "{query}"'
  )
  results_list = parsing.parse_html(results_html, results.metadata)

  #: 5
  logger.info(
    f'Getting municipality data: "{query}"'
  )
  results_list, municip_errors = parsing.get_municipality_data(results_list)

  if municip_errors > 0:
    logger.warning(
      f'Could not pull municipality data of {str(municip_errors)} entry(s)'
    )

  results.results         = results_list
  results.count           = len(results_list)
  results.metadata.status = results.metadata.STATUS_COMPLETE
  return results