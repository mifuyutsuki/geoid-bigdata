from selenium.webdriver.remote.webdriver import WebDriver

from copy import deepcopy
import logging

from geoid.common import io
from geoid.config import Config
from geoid.processing import postproc
from . import processing, query


logger = logging.getLogger(__name__)


class BigQuery:
  def __init__(self, use_config: Config=None):
    self.webdriver = None
    self.config    = use_config if use_config else Config()

    self.data    = None
    self.count   = 0
    self.querier = None
  

  def import_cities(
    self,
    source_filename: str,
    keyword: str
  ):
    data = io.import_json(source_filename)
    data = processing.initialize(keyword, data)
    #: verify?

    self.data    = data
    self.count   = len(data)
    self.querier = None


  def import_save(
    self,
    source_filename: str
  ):
    data = io.import_json(source_filename)
    #: verify?

    self.data    = data
    self.count   = len(data)
    self.querier = None
  

  def export_json(
    self,
    target_filename: str,
    *,
    filter_by_city=False,
    flatten=False,
    convert_ascii=False,
    replace_newline=False,
    indent=1,
    **json_kwargs
  ):
    if self.data is None:
      return
    
    export_data = deepcopy(self.data)

    if filter_by_city  : export_data = postproc.filter_by_city(export_data)
    if flatten         : export_data = postproc.convert_flat(export_data)
    if convert_ascii   : export_data = postproc.convert_ascii(export_data)
    if replace_newline : export_data = postproc.replace_newline(export_data)

    io.export_json(target_filename, export_data, indent=indent, **json_kwargs)


  def autosave(self):
    io.export_json(self.config.fileio.autosave_filename, self.data)


  def initialize(self, webdriver: WebDriver):
    self.webdriver = webdriver
    self.querier   = self._get_one_iter()


  def get_one(self):
    if (self.webdriver is None) or (self.querier is None):
      raise RuntimeError(
        'BigQuery must be initialized with initialize() to begin querying'
      )
    return next(self.querier)


  def _get_one_iter(self):
    if self.config.fileio.autosave_every > 0:
      self.autosave()

    for index, data_object in enumerate(self.data):
      new_object, query_status = query.get_one(data_object, self.webdriver, self.config)

      if new_object is not None:
        self.data[index] = new_object
      
      yield query_status
      