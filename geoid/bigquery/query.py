from selenium.webdriver.remote.webdriver import WebDriver

from copy import deepcopy
import logging

from geoid.config import Config
from geoid.constants import keys, status
from geoid.query import query
from . import io, processing


logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def import_cities(
  source_filename: str,
  keyword: str
):
  data = io.import_json(source_filename)
  data = processing.initialize(keyword, data)
  #: verify?


def get(
  data: list[dict],
  webdriver: WebDriver,
  use_config: Config=None
):
  new_data = deepcopy(data)
  config = use_config if use_config else Config()
  autosave_filename = config.fileio.autosave_filename
  autosave_every    = config.fileio.autosave_every

  #: 1
  if config.fileio.autosave_every > 0:
    autosave(new_data, autosave_filename)
  
  #: 2
  completeds = 0

  for index, data_object in enumerate(new_data):
    #: 2.1
    if (data_object is None) or (keys.QUERY not in data_object):
      continue

    if keys.QUERY_STATUS in data_object:
      if data_object[keys.QUERY_STATUS] == status.QUERY_COMPLETE:
        continue
    
    #: 2.2
    query_ = data_object[keys.QUERY]
    results = query.get(query_, webdriver, use_config=config)

    #: 2.3
    if results.metadata.status == results.metadata.STATUS_COMPLETE:
      completeds = completeds + 1
      data_object.update(results.report())
    
    #: 2.4
    if completeds % autosave_every == 0:
      autosave(new_data, autosave_filename)
  
  #: 3
  if autosave_every > 0:
    autosave(new_data, autosave_filename)
  
  #: 4
  return new_data


def autosave(
  data: list[dict],
  config: Config
):
  io.export_json(
    config.fileio.autosave_filename, data, config.fileio.output_indent
  )