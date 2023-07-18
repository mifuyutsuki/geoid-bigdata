from bs4 import BeautifulSoup

from geoid.constants import Selectors
from . import processing

import logging


logger = logging.getLogger(__name__)


def parse_html(grabbed_html: str, query_lang: str):
  logger.info(
    f'Processing results'
  )
  results = []
  
  results_raw = BeautifulSoup(grabbed_html, 'lxml').select(Selectors.RESULT)

  for result_raw in results_raw:
    if result_raw is not None:
      result = processing.get_entry_fields(
        result_raw, query_lang=query_lang
      )
      results.append(result)
  
  return results


def get_municipality_data(results: list[dict]):
  logger.info(
    f'Getting municipality data'
  )
  new_results = results.copy()
  errors = 0

  for index, result in enumerate(results):
    try:
      new_results[index] = processing.get_municipality_fields(result)
    except Exception as e:
      logger.exception(e)
      errors = errors + 1
      continue
  
  if errors > 0:
    logger.warning(
      f'Could not pull municipality data of {str(errors)} entry(s)'
    )
  
  return new_results, errors