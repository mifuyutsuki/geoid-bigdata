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

from selenium.webdriver.remote.webdriver import WebDriver

import logging

from geoid.config import Config
from geoid.constants import Keys, Status
from geoid.query import query
from geoid.common import io


logger = logging.getLogger(__name__)


def get_iterator(
  queries_data: list[dict],
  webdriver: WebDriver,
  config: Config
):
  queries_count = len(queries_data)
  for index, data_object in enumerate(queries_data):
    logger.info(
      f'Query progress: ({index+1}/{queries_count})'
    )
    new_object, query_status = get_one(
      data_object, webdriver, config
    )
    
    yield new_object, index, query_status
  
  logger.info(
    'Reached end of query'
  )


def get_one(
  data_object: dict,
  webdriver: WebDriver,
  config: Config
):
  #: 1
  if io._is_keyword_missing(data_object):
    logger.warning(
      f'Query skipped due to missing keyword'
    )
    return data_object, Status.QUERY_MISSING
  
  new_object = data_object.copy()
  query_keyword = data_object[Keys.QUERY_KEYWORD]

  if Keys.QUERY_STATUS not in new_object:
    new_object[Keys.QUERY_STATUS] = Status.QUERY_INCOMPLETE
    
  query_status = new_object[Keys.QUERY_STATUS]

  #: 2
  if query_status == Status.QUERY_COMPLETE:
    logger.info(
      f'Query already marked as complete: "{query_keyword}"'
    )
    return new_object, Status.QUERY_COMPLETE
  
  #: 3
  new_object.update(query.get(new_object, webdriver, use_config=config))

  #: 4
  query_status = new_object[Keys.QUERY_STATUS]
  if query_status == Status.QUERY_MISSING:
    logger.warning(
      f'Query skipped due to missing keyword'
    )
  elif query_status == Status.QUERY_ERRORED:
    logger.error(
      f'Could not do query, continuing: "{query_keyword}"'
    )
  elif query_status == Status.QUERY_COMPLETE:
    logger.info(
      f'Completed query: "{query_keyword}"'
    )
  elif query_status == Status.QUERY_COMPLETE_MUNICIPALITIES_MISSING:
    logger.info(
      f'Completed query: "{query_keyword}"'
    )
    logger.warning(
      f'Query contains missing municipality data: "{query_keyword}"'
    )
  
  return new_object, query_status