from selenium.webdriver.remote.webdriver import WebDriver

from copy import deepcopy
import logging

from geoid.common import io
from geoid.config import Config
from geoid.processing import postproc
from geoid.constants import Status
from . import processing, query


logger = logging.getLogger(__name__)


class BigQuery:
  def __init__(self, use_config: Config=None):
    self.webdriver = None
    self.config    = use_config if use_config else Config()

    self.source_filename   = None
    self.target_filename   = None
    self.autosave_filename = None

    self.data    = None
    self.count   = 0
    self.querier = None

    self._progress   = 1
    self._completeds = 0
  

  def import_new(
    self,
    source_filename: str,
    keyword: str
  ):
    data = io.import_json(source_filename)
    data = processing.initialize(keyword, data)
    #: verify?

    self.source_filename = source_filename
    self.data            = data
    self.count           = len(data)
    self.querier         = None

    logger.info(
      f'Imported cities data JSON from "{source_filename}"'
    )


  def import_save(
    self,
    source_filename: str
  ):
    data = io.import_json(source_filename)
    #: verify?

    self.source_filename = source_filename
    self.data            = data
    self.count           = len(data)
    self.querier         = None
    
    logger.info(
      f'Imported save data JSON from "{source_filename}"'
    )

  def export_json(
    self,
    target_filename=None,
    *,
    filter_by_city=None,
    flatten=None,
    convert_ascii=None,
    replace_newline=None,
    indent=None,
    **json_kwargs
  ):
    if self.data is None:
      return
    
    if target_filename is None : target_filename = self.target_filename
    if filter_by_city is None  : filter_by_city  = self.config.postproc.filter
    if flatten is None         : flatten         = self.config.postproc.flatten
    if convert_ascii is None   : convert_ascii   = self.config.postproc.convert_ascii
    if replace_newline is None : replace_newline = self.config.postproc.replace_newline
    if indent is None          : indent          = self.config.fileio.output_indent

    if not isinstance(target_filename, str):
      raise ValueError(f'Invalid filename of type "{str(type(target_filename))}"')
    if not isinstance(indent, int):
      raise ValueError(f'Invalid indent value of type "{str(type(indent))}"')

    if len(target_filename) <= 0:
      raise ValueError(f'Invalid filename of "{target_filename}"')

    export_data = deepcopy(self.data)

    if filter_by_city  : export_data = postproc.filter_by_city(export_data)
    if flatten         : export_data = postproc.convert_flat(export_data)
    if convert_ascii   : export_data = postproc.convert_ascii(export_data)
    if replace_newline : export_data = postproc.replace_newline(export_data)

    io.export_json(
      target_filename, export_data, indent=indent, **json_kwargs
    )
    
    logger.info(
      f'Exported queries data JSON to "{target_filename}"'
    )


  def autosave(self):
    autosave_filename = self.autosave_filename
    if len(autosave_filename) <= 0:
      raise ValueError(f'Unspecified autosave filename of "{autosave_filename}"')
    
    io.export_json(
      autosave_filename, self.data, self.config.fileio.output_indent
    )
    
    logger.info(
      f'Autosaved queries data JSON to "{autosave_filename}"'
    )


  def initialize(self, webdriver: WebDriver):
    self.webdriver = webdriver
    self.querier   = self._get_one_iter()
    self._progress = 1


  def get_one(self):
    if (self.webdriver is None) or (self.querier is None):
      raise RuntimeError(
        'BigQuery must be initialized with initialize() to begin querying'
      )
    
    logger.info(
      f'Query progress: ({str(self._progress)}/{str(self.count)})'
    )
    query_status   = next(self.querier)
    self._progress = self._progress + 1

    if query_status == Status.QUERY_MISSING:
      logger.warning(
        f'Query object {str(self._progress)}/{str(self.count)} skipped '
        f'due to missing query'
      )

    if query_status == Status.QUERY_COMPLETE or \
    query_status == Status.QUERY_COMPLETE_MUNICIPALITIES_MISSING:
      self._completeds = self._completeds + 1
      if self._completeds % self.config.fileio.autosave_every == 0:
        self.autosave()
    
    return query_status


  def _get_one_iter(self):
    if self.config.fileio.autosave_every > 0:
      self.autosave()

    for index, data_object in enumerate(self.data):
      new_object, query_status = query.get_one(data_object, self.webdriver, self.config)

      if new_object is not None:
        self.data[index] = new_object
      
      yield query_status