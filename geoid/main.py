from selenium import webdriver
from selenium.common.exceptions import *
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
  querier_config.autosave_every = 1
  querier_config.keep_autosave = False
  querier_config.query_depth = query_depth

  if use_timestamp:
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    output_file = output_file.replace("{timestamp}", timestamp)

  querier = BigQuerier(
    source_file,
    output_file,
    use_config=querier_config
  )

  logger.info('Initializing webdriver')
  try:
    driver = _initialize_driver(web_client, show_client=show_client)
  except WebDriverException as e:
    logger.exception(e)
    logger.error(
      'Unable to initialize webdriver'
    )
    quit()
  except Exception as e:
    logger.exception(e)
    quit()
  else:
    logger.info('Initialized webdriver')

  try:
    querier.begin(
      driver,
      keyword
    )
  except Exception as e:
    logger.error(str(e))
    raise
  finally:
    logger.info('Terminating webdriver')
    driver.quit()
    logger.info('Terminated webdriver')

  if querier.outputs_count <= 0:
    logger.info('No query results to process further')
  else:
    if use_postprocess:
      querier.postprocess()
    querier.export_json(indent=indent)

def _initialize_driver(web_client: str, *, show_client=False):
  if web_client.lower() == 'firefox':
    options = webdriver.FirefoxOptions()
    if not show_client:
      options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
  
  elif web_client.lower() == 'chrome':
    options = webdriver.ChromeOptions()
    if not show_client:
      options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
  
  else:
    raise ValueError(f'Invalid or unsupported web client: {web_client}')

  return driver