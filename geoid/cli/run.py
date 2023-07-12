from selenium.common.exceptions import *

from geoid.bigquery import BigQuery
from geoid.common import webclient
from geoid.config import Config
from geoid.logging import LOG_CONFIG
import logging, logging.config, os


logger = logging.getLogger(__name__)


def run_batch(
  keyword: str,
  source_file: str,
  output_file: str,
  *,
  use_config:Config=None
):
  """
  Launch a batch query for "keyword cityname" for citynames in `source_file`.

  Launch `keyword` and list of city names given in JSON file `source_file`,
  start a batch query for "keyword cityname" and output its results to JSON
  file `output_file`.
  
  Using `use_config` settings, query results may be postprocessed, for example
  to filter for city-mismatched results and/or flatten to a single-layered JSON
  array of objects.

  In addition, the function may also create unpostprocessed autosave file
  `output_file.autosave` as well as log file `./logs/timestamp.log`. This may
  be changed in `use_config`.

  Args:
      keyword (str): Query keyword which will prepend the citynames.
      source_file (str): Input JSON file containing citynames.
      output_file (str): Output JSON file containing query results.

  Kwargs:
      use_config (Config): Config object containing advanced query and program
      settings.
  """

  #: Initialize logging
  if not os.path.exists(r'./logs/'):
    os.mkdir(r'./logs/')

  logging.config.dictConfig(LOG_CONFIG)

  config = use_config if use_config else Config()

  #: Initialize querying
  querier = BigQuery(config)
  querier.target_filename   = output_file
  querier.autosave_filename = output_file + '.autosave'

  querier.import_new(source_file, keyword)

  if querier.count <= 0:
    logger.warning(
      'No queries to start'
    )
    return

  #: Initialize web client
  logger.info('Initializing web client')
  try:
    driver = init_webclient(config)
    querier.initialize(driver)
  except WebDriverException as e:
    logger.exception(e)
    logger.error(
      'Unable to initialize web client'
    )
    return
  except Exception as e:
    logger.exception(e)
    return
  else:
    logger.info('Initialized web client')

  #: Query
  try:
    querier = get_all(querier)
  finally:
    logger.info('Terminating web client')
    driver.quit()
    logger.info('Terminated web client')

  querier.report_log()

  #: Export
  if querier.count > 0:
    querier.export_json(output_file)
  else:
    logger.info('No entries to export')


def init_webclient(config: Config):
  """
  Initialize a Selenium web client.

  Receive input from config value `config.webclient.webclient`, then initialize
  a Selenium webdriver controlling the web client.

  Args:
      config: Config object containing advanced query settings.
  
  Returns:
      Selenium webdriver controlling the web client.
  
  Raises
      ValueError: Web client provided in `config` doesn't exist or is
      unsupported by GeoID.
      WebDriverException: Web client failed to initialize. May occur when the
      web client closed itself to update.
  """

  use_client  = config.webclient.webclient.lower().strip()
  show_client = config.webclient.show
  if use_client == 'firefox':
    driver = webclient.init_firefox(show_client=show_client)
  elif use_client == 'chrome':
    driver = webclient.init_chrome(show_client=show_client)
  else:
    raise ValueError(
      f'Webclient "{use_client}" does not exist or is unsupported'
    )

  return driver


def get_all(querier: BigQuery):
  running = True

  while running:
    try:
      querier.get_one()
    except StopIteration:
      running = False
    except Exception as e:
      logger.error(str(e))
      continue
  
  return querier