from selenium.common.exceptions import *
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from urllib.parse import quote_plus
from time import sleep
import logging

from geoid.config import Config
from geoid.constants import Selectors, Links


logger = logging.getLogger(__name__)

INFINITE_SCROLL = 0
SCROLL_SUCCESS = 0
SCROLL_FAILURE = 1
SCROLL_END     = 2


def get(
  query: str,
  webdriver: WebDriver,
  config: Config,
  *,
  use_lang: str=None
):
  lang = use_lang if use_lang else config.query.lang

  #: Get query
  logger.info(
    f'Starting query: "{query}"'
  )
  webdriver.get(
    Links.GMAPS_QUERY_TARGET.format(
      query=quote_plus(query),
      query_lang=quote_plus(lang)
    )
  )

  #: Pause if initial pause is set
  if config.query.initial_pause_seconds > 0:
    logger.info(
      f'Pausing for {str(config.query.initial_pause_seconds)} second(s) '
      f'per configuration'
    )
    sleep(config.query.initial_pause_seconds)

  #: Detect CAPTCHA box
  if len(webdriver.find_elements(
    By.CSS_SELECTOR, Selectors.RECAPTCHA
  )) > 0:
    logger.error(
      'Failed to load page (CAPTCHA)'
    )
    raise RuntimeError('Failed to load page: CAPTCHA')

  #: Ensure page is sufficiently loaded
  try:
    WebDriverWait(
      webdriver, config.query.loading_timeout_seconds
    ) \
    .until(
      lambda d:
        d.find_element(By.CSS_SELECTOR, Selectors.SEARCHBOX)
    )
  except TimeoutException:
    logger.error(
      'Failed to load page (timed out)'
    )
    raise

  #: Check for results box
  try:
    webdriver.find_element(
      By.CSS_SELECTOR, Selectors.RESULTS_BOX
    )
  except NoSuchElementException:
    logger.error(
      'Could not find results box; '
      'query may have outputted a location instead of search results'
    )
    raise

  return webdriver


def scroll(
  webdriver: WebDriver,
  config: Config
):
  logger.info(
    f'Scrolling query'
  )
  scrolls_remaining = config.query.depth - 1
  retries_remaining = config.query.scroll_retries
  scroll_status = SCROLL_FAILURE

  while (
    (
      config.query.depth == INFINITE_SCROLL or
      scrolls_remaining > 0
    ) and \
    retries_remaining > 0
  ):
    #: Detect end-of-scroll and other exceptions
    try:
      scroll_status = _scroll_one(webdriver, config)
    except Exception:
      break

    if (
      scroll_status == SCROLL_SUCCESS and
      config.query.depth == INFINITE_SCROLL
    ):
      retries_remaining = config.query.scroll_retries

    elif (
      scroll_status == SCROLL_SUCCESS and
      config.query.depth != INFINITE_SCROLL
    ):
      scrolls_remaining = scrolls_remaining - 1
      retries_remaining = config.query.scroll_retries

    else:
      retries_remaining = retries_remaining - 1
  
  #: End of while loop, post debug log
  if scrolls_remaining == 0 and retries_remaining > 0:
    logger.debug('Scroll completed (depth reached)')
  elif scrolls_remaining > 0 and retries_remaining == 0:
    logger.debug('Scroll completed (out of scroll retries)')
  else:
    logger.debug('Scroll completed')
  
  return webdriver


def _scroll_one(
  webdriver: WebDriver,
  config: Config
):
  results_count_before = _count_results(webdriver)

  #: Produces NoSuchElementException on reaching end-of-list.
  #: Used to mark end of query
  webdriver.find_element(By.CSS_SELECTOR, Selectors.RESULTS_BOTTOM)

  #: move_to_element() of out-of-viewport elements produces errors
  #: when using Firefox webdriver. Worked around by executing JS
  #: Case ex. https://stackoverflow.com/a/68676754
  result_elements = webdriver.find_elements(
    By.CSS_SELECTOR, Selectors.GENERAL_RESULT
  )
  last_result_element = result_elements[-1]
  webdriver.execute_script(
    "arguments[0].scrollIntoView(true);", last_result_element
  )
  sleep(config.query.scroll_wait_seconds)

  results_count_after = _count_results(webdriver)

  if results_count_after > results_count_before:
    return_status = SCROLL_SUCCESS
  else:
    return_status = SCROLL_FAILURE
    
  return return_status


def _count_results(webdriver: WebDriver):
  return len(
    webdriver.find_elements(
      By.CSS_SELECTOR, Selectors.GENERAL_RESULT
    )
  )


def grab(webdriver: WebDriver):
  return webdriver.find_element(
    By.CSS_SELECTOR, Selectors.RESULTS_BOX
  ).get_attribute('innerHTML')