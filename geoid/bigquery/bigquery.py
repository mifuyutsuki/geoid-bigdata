from selenium.webdriver.remote.webdriver import WebDriver

from copy import deepcopy
import logging

from geoid.common import io
from geoid.config import Config
from geoid.processing import postproc
from geoid.constants import Status, Keys
from . import processing, query


logger = logging.getLogger(__name__)


class BigQuery:
  ZERO_STATUS_COUNTS = {
    Status.QUERY_INCOMPLETE                      : 0,
    Status.QUERY_MISSING                         : 0,
    Status.QUERY_ERRORED                         : 0,
    Status.QUERY_COMPLETE                        : 0,
    Status.QUERY_COMPLETE_MUNICIPALITIES_MISSING : 0
  }

  ZERO_STATUS_OBJECTS = {
    Status.QUERY_INCOMPLETE                      : [],
    Status.QUERY_MISSING                         : [],
    Status.QUERY_ERRORED                         : [],
    Status.QUERY_COMPLETE                        : [],
    Status.QUERY_COMPLETE_MUNICIPALITIES_MISSING : []
  }
  
  def __init__(self, use_config: Config=None):
    self.webdriver = None
    self.config    = use_config if use_config else Config()

    self.source_filename   = None
    self.target_filename   = None
    self.autosave_filename = None

    self.data    = None
    self.querier = None

    self._progress      = 0
    self._count         = 0
    self._status_counts = self.ZERO_STATUS_COUNTS
  

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
    self.querier         = None

    self._progress       = 0
    self._count          = len(data)
    self._status_counts  = self.ZERO_STATUS_COUNTS

    for data_object in data:
      object_status = processing.report_object(data_object)
      self._status_counts[object_status] += 1

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
    self.querier         = None
    
    self._progress       = 0
    self._count          = len(data)
    self._status_counts  = self.ZERO_STATUS_COUNTS

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
      raise ValueError(
        f'Invalid filename of type "{str(type(target_filename))}"'
      )
    if not isinstance(indent, int):
      raise ValueError(
        f'Invalid indent value of type "{str(type(indent))}"'
      )

    if len(target_filename) <= 0:
      raise ValueError(
        f'Invalid filename of "{target_filename}"'
      )

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
      raise ValueError(
        f'Unspecified autosave filename of "{autosave_filename}"'
      )
    
    io.export_json(
      autosave_filename, self.data, self.config.fileio.output_indent
    )
    
    logger.info(
      f'Autosaved queries data JSON to "{autosave_filename}"'
    )


  def initialize(self, webdriver: WebDriver):
    self.webdriver      = webdriver
    self.querier        = self._get_one_iter()
    self._progress      = 0
    self._status_counts = self.ZERO_STATUS_COUNTS


  def get_one(self):
    if (self.webdriver is None) or (self.querier is None):
      raise RuntimeError(
        'BigQuery must be initialized with initialize() to begin querying'
      )
    if self._progress >= self._count:
      logger.info(
        'Reached end of query'
      )
      self.report_log()
      raise StopIteration('Reached end of query')
    
    index = self._progress
    self._progress = index + 1
    logger.info(
      f'Query progress: ({str(self._progress)}/{str(self._count)})'
    )

    query_status = next(self.querier)
    self._status_counts[query_status] += 1

    if query_status == Status.QUERY_MISSING:
      logger.warning(
        f'Query object {str(self._progress)}/{str(self._count)} skipped '
        f'due to missing query'
      )
    
    elif query_status == Status.QUERY_ERRORED:
      logger.error(
        f'Could not complete query {str(self._progress)}/{str(self._count)}'
      )

    elif query_status == Status.QUERY_COMPLETE:
      logger.info(
        f'Completed query {str(self._progress)}/{str(self._count)}'
      )
      if self._progress % self.config.fileio.autosave_every == 0:
        self.autosave()
    
    elif query_status == Status.QUERY_COMPLETE_MUNICIPALITIES_MISSING:
      logger.info(
        f'Completed query {str(self._progress)}/{str(self._count)}'
      )
      logger.warning(
        f'Query {str(self._progress)}/{str(self._count)} '
        f'contains missing municipality data'
      )
      if self._progress % self.config.fileio.autosave_every == 0:
        self.autosave()
    
    return query_status


  def _get_one_iter(self):
    if self.config.fileio.autosave_every > 0:
      self.autosave()

    for index, data_object in enumerate(self.data):
      new_object, query_status = query.get_one(
        data_object, self.webdriver, self.config
      )

      if new_object is not None:
        self.data[index] = new_object
      
      yield query_status
  

  def report_log(self):
    queries_progress                  = self._progress
    queries_count                     = self._count
    queries_missing                   = self._status_counts[Status.QUERY_MISSING]
    queries_errored                   = self._status_counts[Status.QUERY_ERRORED]
    queries_complete                  = self._status_counts[Status.QUERY_COMPLETE]
    queries_complete_municips_missing = self._status_counts[Status.QUERY_COMPLETE_MUNICIPALITIES_MISSING]

    logger.info(
      f'Report: {str(queries_progress)} processed, {str(queries_count)} object(s)'
    )
    logger.info(
      f'{str(queries_complete + queries_complete_municips_missing)} completed '
      f'({str(queries_complete_municips_missing)} with missing municips)'
    )
    logger.info(
      f'{str(queries_missing)} missing, {str(queries_errored)} error(s)'
    )

  
  def report_list(self):
    report_entries   = []
    new_report_entry = {
      Keys.REPORT_NO     : 0,
      Keys.REPORT_QUERY  : None,
      Keys.REPORT_STATUS : None
    }
    report_categories = self.ZERO_STATUS_OBJECTS.copy()

    for index, data_object in enumerate(self.data):
      report_entry = new_report_entry.copy()
      report_entry[Keys.REPORT_NO] = index + 1

      if Keys.QUERY in data_object:
        report_entry[Keys.REPORT_QUERY] = data_object[Keys.QUERY]
        report_entry[Keys.REPORT_STATUS] = data_object[Keys.QUERY_STATUS]
      else:
        report_entry[Keys.REPORT_STATUS] = Status.QUERY_MISSING

      report_entries.append(report_entry)
      report_categories[data_object[Keys.QUERY_STATUS]].append(str(index + 1))
    
    return report_entries
  

  def report_json(self, filename: str):
    report_data = self.report_list()

    io.export_json(
      filename, report_data, self.config.fileio.output_indent
    )
    
    logger.info(
      f'Exported queries report data JSON to "{filename}"'
    )
  

  @property
  def count(self):
    return self._count
  
  @property
  def progress(self):
    return self._progress