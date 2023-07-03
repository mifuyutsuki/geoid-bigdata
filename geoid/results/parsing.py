from bs4 import BeautifulSoup

from geoid.constants import cselectors
from geoid import processing
from .metadata import Metadata

import logging

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

def parse_html(grabbed_html: str, metadata: Metadata):
  results = []
  
  results_raw = BeautifulSoup(grabbed_html, 'lxml').select(cselectors.RESULT)

  for result_raw in results_raw:
    if result_raw is not None:
      result = processing.results.proc_entry(
        result_raw, query_lang=metadata.lang
      )
      results.append(result)
  
  return results

def get_municipality_data(results: list):
  new_results = results.copy()
  errors = 0

  for result in new_results:
    try:
      result = processing.results.proc_municipality(result)
    except Exception as e:
      logger.error(str(e))
      errors = errors + 1
      continue
  
  return new_results, errors