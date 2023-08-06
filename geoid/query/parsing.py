# Copyright (c) 2023 Mifuyu (mifuyutsuki@proton.me)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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