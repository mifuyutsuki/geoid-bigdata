from selenium import webdriver
from . import BigQuerier, BigQuerierConfig, LOG_CONFIG
import logging, logging.config, time

def begin(
  keyword: str,
  source_file: str,
  output_file: str,
  *,
  query_depth=0,
  indent=1,
  web_client='firefox',
  show_client=False,
  use_postprocess=True,
  use_timestamp=True
):
  logging.config.dictConfig(LOG_CONFIG)
  logger = logging.getLogger('geoid')

  querier_config = BigQuerierConfig()
  querier_config.scroll_wait_seconds = 1.1

  if use_timestamp:
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    output_file = output_file.replace("{timestamp}", timestamp)

  querier = BigQuerier(
    source_file,
    output_file,
    use_config=querier_config
  )

  logger.info('Initializing webdriver')
  if web_client == 'firefox':
    driver = _initialize_driver_firefox(show_client=show_client)
  elif web_client == 'chrome':
    driver = _initialize_driver_chrome(show_client=show_client)
  logger.info('Initialized webdriver')

  try:
    querier.begin(
      driver,
      keyword,
      query_depth=query_depth
    )
  except Exception as e:
    logger.error(str(e))
    raise
  finally:
    logger.info('Terminating webdriver')
    driver.quit()
    logger.info('Terminated webdriver')

  if use_postprocess:
    querier.postprocess()

  querier.export_json(indent=indent)

def _initialize_driver_firefox(*, show_client=False):
  options = webdriver.FirefoxOptions()
  if not show_client:
    options.add_argument('-headless')
  driver = webdriver.Firefox(options=options)
  return driver

def _initialize_driver_chrome(*, show_client=False):
  options = webdriver.ChromeOptions()
  if not show_client:
    options.add_argument('-headless')
  driver = webdriver.Chrome(options=options)
  return driver