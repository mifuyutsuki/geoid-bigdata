from selenium import webdriver
from selenium.common.exceptions import *
from . import BigQuerier
from .config import Config
from .logging import LOG_CONFIG
import logging, logging.config, time

def begin(
  keyword: str,
  source_file: str,
  output_file: str,
  *,
  use_config:Config=None
):
  logging.config.dictConfig(LOG_CONFIG)
  logger = logging.getLogger('geoid')

  config = use_config if use_config else Config()

  if config.fileio.use_timestamp_name:
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    output_file = output_file.replace("{timestamp}", timestamp)

  querier = BigQuerier(
    source_file,
    output_file,
    use_config=config
  )

  logger.info('Initializing webdriver')
  try:
    driver = _initialize_driver(
      config.webclient.webclient,
      show_client=config.webclient.show
    )
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
    querier.postprocess()
    querier.export_json(indent=config.fileio.output_indent)

def _initialize_driver(webclient: str, *, show_client=False):
  if webclient.lower() == 'firefox':
    options = webdriver.FirefoxOptions()
    if not show_client:
      options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
  
  elif webclient.lower() == 'chrome':
    options = webdriver.ChromeOptions()
    if not show_client:
      options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
  
  else:
    raise ValueError(f'Invalid or unsupported web client: {webclient}')

  return driver