from selenium import webdriver
from bigquery.bigquerier import BigQuerier
import sys, logging, time

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s',
  stream=sys.stdout
)

def initialize_driver():
  options = webdriver.FirefoxOptions()
  options.add_argument('-headless')
  driver = webdriver.Firefox(options=options)
  return driver

def main():
  keyword = 'pariwisata'
  input_json_file = r'input_data\sample_cities_data.json'

  logger = logging.getLogger('test_sample')
  logger.setLevel(logging.INFO)
  
  logger.info('Initializing webdriver')
  driver = initialize_driver()
  logger.info('Initialized webdriver')

  querier = BigQuerier(driver, input_json_file)
  try:
    querier.begin(keyword=keyword, query_depth=1)
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