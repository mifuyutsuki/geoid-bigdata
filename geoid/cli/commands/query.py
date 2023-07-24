from selenium.common.exceptions import *

from geoid.bigquery import BigQuery
from geoid.common import webclient
from geoid.config import Config
from geoid.logging import log_start
import logging, logging.config, time


logger = logging.getLogger(__name__)


def start_query(args):
  if args.timestamp:
    if "{timestamp}" not in args.outputfile:
      print(
        'Specify timestamp location in the output filename using {timestamp} '
        'to use the timestamp option'
      )
      return
    else:      
      timestamp = time.strftime('%Y%m%d_%H%M%S')
      output_file = args.outputfile.replace("{timestamp}", timestamp)
  else:
    output_file = args.outputfile
  
  config = Config()
  config.query.depth                 = args.depth
  config.fileio.output_indent        = args.indent
  config.webclient.webclient         = args.browser
  config.query.initial_pause_seconds = args.init_pause
  config.webclient.show              = args.show
  config.fileio.use_timestamp_name   = args.timestamp
  config.fileio.keep_autosave        = args.keep_autosave
  config.postproc.filter             = args.filter
  config.postproc.flatten            = args.flatten
  config.postproc.convert_ascii      = args.convert_ascii
  config.postproc.replace_newline    = args.replace_newline

  print(
    f'Launching query, source file: {args.sourcefile}.'
  )
  log_start()
  run_batch(
    source_file=args.sourcefile,
    output_file=output_file,
    use_config=config
  )


def run_batch(
  source_file: str,
  output_file: str,
  *,
  use_config:Config=None
):
  """
  Launch a query for "term cityname" for citynames in file `source_file`.

  Given `term` and list of city names given in JSON file `source_file`,
  start a batch query for "term cityname" and output its results to JSON
  file `output_file`.
  
  Using `use_config` settings, query results may be postprocessed, for example
  to filter for city-mismatched results and/or flatten to a single-layered JSON
  array of objects.

  In addition, the function may also create unpostprocessed autosave file
  `output_file.autosave` as well as log file `./logs/timestamp.log`. This may
  be changed in `use_config`.

  Args:
      term (str): Query term which will prepend the citynames.
      source_file (str): Input JSON file containing citynames.
      output_file (str): Output JSON file containing query results.

  Kwargs:
      use_config (Config): Config object containing advanced query and program
      settings.
  """

  config = use_config if use_config else Config()

  querier = BigQuery(config)
  querier.target_filename   = output_file
  querier.autosave_filename = output_file + '.autosave'

  querier.import_data(source_file)

  _run(querier, config)


def _run(querier: BigQuery, config: Config):
  if querier.count <= 0:
    return

  #: Initialize web client
  logger.info('Initializing web client')
  try:
    driver = _init_webclient(config)
    querier.initialize(driver)
  except Exception as e:
    logger.exception(e)
    return
  else:
    logger.info('Initialized web client')

  #: Query
  try:
    querier = _get_all(querier)
  finally:
    logger.info('Terminating web client')
    driver.quit()
    logger.info('Terminated web client')

  querier.report_log()

  #: Export
  if querier.count > 0:
    querier.export_json(querier.target_filename)
  else:
    logger.info('No entries to export')
  querier.remove_autosave_if_set()


def _init_webclient(config: Config):
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


def _get_all(querier: BigQuery):
  running = True

  while running:
    try:
      querier.get_one()
    except StopIteration:
      running = False
    except Exception as e:
      logger.error(str(e))
      continue
    
    if querier.progress == querier.count:
      running = False
  
  return querier