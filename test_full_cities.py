from selenium import webdriver
from geoid import BigQuerier
import logging, logging.config, time

log_format = '[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
log_starttime = time.strftime('%Y%m%d_%H%M%S')
log_filename = r'logs\{0}.log'.format(log_starttime)

#: Using DEBUG causes logging errors due to selenium logging the HTML, which
#: contains special Unicode characters. (The program can continue, though.)
log_config = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "simple": {
      "format": '[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "stream": "ext://sys.stdout",
      "level": "INFO",
      "formatter": "simple"
    },
    "file": {
      "class": "logging.FileHandler",
      "filename": log_filename,
      "mode": "w",
      "level": "INFO",
      "formatter": "simple"
    }
  },
  "root": {
    "level": "INFO",
    "handlers": ["console", "file"]        
  }
}

logging.config.dictConfig(log_config)
logger = logging.getLogger('main')

# =============================================================================

def initialize_driver(*, start_headless=True):
  options = webdriver.FirefoxOptions()
  if start_headless:
    options.add_argument('-headless')
  driver = webdriver.Firefox(options=options)
  return driver

def main():
  keyword = 'pariwisata'
  input_json_file = r'input_data\cities_data_1of3.json'

  querier = BigQuerier(
    input_json_file,
    scroll_wait_seconds=1.1
  )
  
  logger.info('Initializing webdriver')
  driver = initialize_driver()
  logger.info('Initialized webdriver')

  try:
    querier.begin(
      driver,
      keyword,
      query_depth=0
    )
  except Exception as e:
    logger.error(str(e))
    raise
  finally:
    logger.info('Terminating webdriver')
    driver.quit()
    logger.info('Terminated webdriver')

  querier.postprocess()
  
  output_time = time.strftime('%Y%m%d_%H%M%S')
  output_json_file = r'output_data\query_{0}_{1}.json'.format(keyword, output_time)
  querier.export_json(output_json_file, indent=1)

if __name__ == '__main__':
    main()