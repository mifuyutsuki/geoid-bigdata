from selenium.common.exceptions import *
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote_plus
from time import time, sleep
import logging

from .results import Results

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

class Querier():
  __SCROLL_SUCCESS = 0
  __SCROLL_FAILURE = 1

  def __init_selectors(self):
    #: Some class names do contain trailing whitespaces; however,
    #: class trailing whitespaces in the HTML fed to bs4 are removed

    #: Results selectors
    self.__RESULT_SELECTOR = 'div[class="Nv2PK THOPZb CpccDe "]'
    self.__RESULTS_BOX_SELECTOR = 'div[class="m6QErb DxyBCb kA9KIf dS8AEf ecceSd "]'
    self.__RESULTS_BOTTOM_SELECTOR = 'div[class="lXJj5c Hk4XGb "]'
    # self.__RESULTS_END_SELECTOR = 'div[class="m6QErb tLjsW eKbjU "]'

    #: Location selectors (unused, kept for reference)
    # self.__LOCATION_INFO_SELECTOR = 'div[class="MngOvd fontBodyMedium zWArOe "]'

  def __init__(self,
    webdriver: WebDriver,
    *,
    loading_timeout_seconds=15.0,
    scroll_wait_seconds=2.5,
    scroll_retries=5
  ):    
    self.__init_selectors()
    self._query           = None
    self._query_depth     = None
    self._query_language  = None
    self._query_timestamp = None

    self.webdriver               = webdriver
    self.loading_timeout_seconds = loading_timeout_seconds
    self.scroll_wait_seconds     = scroll_wait_seconds
    self.scroll_retries          = scroll_retries

  def begin(self,
    query: str, /,
    query_depth=1,
    query_language='id'
  ):
    if len(query) <= 0:
      raise ValueError('Query key must not be empty')
    if query_depth < 0:
      raise ValueError(f'Invalid query count of {query_depth}')
    
    self._query = query
    self._query_depth = query_depth
    self._query_language = query_language
    self._query_timestamp = int(time())

    logger.debug(
      f'Querying: "{query}"' + \
      f', language: {query_language}'
    )
    self.webdriver.get(
      f'https://www.google.com/maps?q={quote_plus(query)}&hl={quote_plus(query_language)}'
    )
  
  def grab_results(self):
    logger.debug(
      f'Grabbing search results: "{self._query}"'
    )
    try:
      self.webdriver.find_element(
        By.CSS_SELECTOR, self.__RESULTS_BOX_SELECTOR
      )
      WebDriverWait(
        self.webdriver, self.loading_timeout_seconds
      ) \
      .until(
        lambda d:
          d.find_element(By.CSS_SELECTOR, self.__RESULTS_BOTTOM_SELECTOR)
      )
    except NoSuchElementException:
      logger.error(
        'Could not find results box; '
        'query may have outputted a location instead of search results'
      )
      raise
    except Exception as e:
      logger.exception(e)
      raise
    
    #: Query depth of 1 --> only grab the first "page", no scroll needed
    if self._query_depth != 1:
      if self._query_depth==self.INFINITE_SCROLL:
        log_depth = 'infinite'
      else:
        log_depth = str(self._query_depth)
      logger.debug(
        f'Starting scrolling, depth: {log_depth}'
      )
      self._scroll_results()
    
    query_element = self.webdriver.find_element(
      By.CSS_SELECTOR, self.__RESULTS_BOX_SELECTOR
    )
    grabbed_html = query_element.get_attribute('innerHTML')

    query_final_count = self._count_results()
    logger.info(
      f'Completed query: "{self._query}"'
    )
    logger.info(
      f'Found {str(query_final_count)} entry(s)'
    )

    return Results(
      grabbed_html,
      self._query,
      self._query_language,
      self._query_timestamp
    )

  def _count_results(self):
    try:
      results = self.webdriver.find_elements(
        By.CSS_SELECTOR, self.__RESULT_SELECTOR
      )
    except NoSuchElementException:
      return 0
    
    results_count = len(results)
    return results_count

  def _scroll_results(self):
    scrolls_remaining = self._query_depth - 1
    retries_remaining = self.scroll_retries

    while (
      (
        self._query_depth == self.INFINITE_SCROLL
        or scrolls_remaining > 0
      ) \
      and retries_remaining > 0
    ):
      #: Captures NoSuchElementException from the function, which marks
      #: end-of-list - exit the while loop
      try:
        scroll_status, results_count = self._scroll_results_once()
      except NoSuchElementException:
        logger.debug('Scroll - reached end of list, scroll completed')
        break

      if (
        scroll_status == self.__SCROLL_SUCCESS and
        self._query_depth == self.INFINITE_SCROLL
      ):
        logger.debug(
          'Scroll - Success' + \
          f' ({str(results_count)} entries, infinite scroll)'
        )
        retries_remaining = self.scroll_retries

      elif (
        scroll_status == self.__SCROLL_SUCCESS and
        self._query_depth != self.INFINITE_SCROLL
      ):
        scrolls_remaining = scrolls_remaining - 1
        logger.debug(
          'Scroll - Success' + \
          f' ({str(results_count)} entries' + \
          f', {str(scrolls_remaining)} scroll(s) left)'
        )
        retries_remaining = self.scroll_retries

      else:
        retries_remaining = retries_remaining - 1
        logger.debug(
          'Scroll - Failure' + \
          f' ({str(results_count)} entries, {str(retries_remaining)} retry(s) left)'
        )
    
    #: End of while loop
    if scrolls_remaining == 0 and retries_remaining > 0:
      logger.debug('Scroll - Completed (depth reached)')
    elif scrolls_remaining > 0 and retries_remaining == 0:
      logger.debug('Scroll - Completed (out of scroll retries)')
    else:
      logger.debug('Scroll - Completed')

  def _scroll_results_once(self):
    results_count_before = self._count_results()

    #: Produces NoSuchElementException on reaching end-of-list.
    #: Used to mark end of query
    self.webdriver.find_element(By.CSS_SELECTOR, self.__RESULTS_BOTTOM_SELECTOR)

    #: move_to_element() of out-of-viewport elements produces errors
    #: when using Firefox webdriver. Worked around by executing JS
    #: Case ex. https://stackoverflow.com/a/68676754
    result_elements = self.webdriver.find_elements(
      By.CSS_SELECTOR, self.__RESULT_SELECTOR
    )
    last_result_element = result_elements[-1]
    self.webdriver.execute_script(
      "arguments[0].scrollIntoView(true);", last_result_element
    )
    sleep(self.scroll_wait_seconds)

    results_count_after = self._count_results()

    if results_count_after > results_count_before:
      return_status = self.__SCROLL_SUCCESS
    else:
      return_status = self.__SCROLL_FAILURE
    return return_status, results_count_after
  
  @property
  def INFINITE_SCROLL(self):
      return 0
