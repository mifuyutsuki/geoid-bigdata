from bs4 import BeautifulSoup

from geoid.constants import Selectors
from . import metadata, processing

import logging


logger = logging.getLogger(__name__)


def parse_html(grabbed_html: str, metadata: metadata.Metadata):
  logger.info(
    f'Processing results'
  )
  results = []
  
  results_raw = BeautifulSoup(grabbed_html, 'lxml').select(Selectors.RESULT)

  for result_raw in results_raw:
    if result_raw is not None:
      result = processing.get_entry_fields(
        result_raw, query_lang=metadata.lang
      )
      results.append(result)
  
  return results


def get_municipality_data(results: list):
  logger.info(
    f'Getting municipality data'
  )
  new_results = results.copy()
  errors = 0

  for result in new_results:
    try:
      result = processing.get_municipality_fields(result)
    except Exception as e:
      logger.exception(e)
      errors = errors + 1
      continue
  
  if errors > 0:
    logger.warning(
      f'Could not pull municipality data of {str(errors)} entry(s)'
    )
  
  return new_results, errors