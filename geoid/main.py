from selenium.common.exceptions import *

from geoid.bigquery import BigQuery
from geoid.common import webclient
from geoid.config import Config
from geoid.logging import LOG_CONFIG
import logging, logging.config, time

logger = logging.getLogger(__name__)

def init_webclient(config: Config):
  use_client  = config.webclient.webclient.lower().strip()
  show_client = config.webclient.show
  if use_client == 'firefox':
    driver = webclient.init_firefox(show_client=show_client)
  elif use_client == 'chrome':
    driver = webclient.init_chrome(show_client=show_client)
  else:
    raise ValueError(
      f'Webclient "{use_client}" is unsupported or does not exist'
    )

  return driver


def get_all(querier: BigQuery):
  while True:
    try:
      querier.get_one()
    except StopIteration:
      break
    except Exception as e:
      logger.error(str(e))
      continue
  
  return querier


def begin(
  keyword: str,
  source_file: str,
  output_file: str,
  *,
  use_config:Config=None
):
  logging.config.dictConfig(LOG_CONFIG)

  config = use_config if use_config else Config()

  if config.fileio.use_timestamp_name:
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    output_file = output_file.replace("{timestamp}", timestamp)

  querier = BigQuery(config)
  querier.target_filename   = output_file
  querier.autosave_filename = output_file + '.autosave'

  querier.import_cities(source_file, keyword)

  logger.info('Initializing web client')
  try:
    driver = init_webclient(config)
    querier.initialize(driver)
  except WebDriverException as e:
    logger.exception(e)
    logger.error(
      'Unable to initialize web client'
    )
    quit()
  except Exception as e:
    logger.exception(e)
    quit()
  else:
    logger.info('Initialized web client')

  try:
    querier = get_all(querier)
  finally:
    logger.info('Terminating web client')
    driver.quit()
    logger.info('Terminated web client')

  querier.export_json(output_file)