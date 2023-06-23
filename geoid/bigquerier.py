from selenium.common.exceptions import *
from selenium.webdriver.remote.webdriver import WebDriver
import json, logging, os

from .querier import Querier
from .constants import keys
from . import processing

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger('BigQuerier')

class BigQuerierConfig:
  def __init__(self):
    self.loading_timeout_seconds = 15.0
    self.scroll_wait_seconds     = 2.5
    self.scroll_retries          = 5

class BigQuerier:
  def __init__(
    self,
    source_filename: str,
    output_filename: str,
    *,
    use_config: BigQuerierConfig = None
  ):
    self._output_data = []
    with open(source_filename, 'r', encoding='UTF-8') as json_file:
      self._input_data = json.load(json_file)
    
    if type(self._input_data) is not list:
      raise ValueError(f'Query file "{source_filename}" must be an array of objects')

    logger.info(
      f'Imported queries file "{source_filename}"'
    )

    self.queries_count = len(self._input_data)
    self.outputs_count = 0
    self.missing_count = 0
    self.errored_count = 0
    self.missing_data  = []
    self.errored_data  = []

    logger.info(
      f'Found {str(self.queries_count)} query object(s)'
    )
    self._detect_missing_query_terms()

    self.webdriver = None
    self.querier   = None
    
    self.source_filename = source_filename
    self.output_filename = output_filename
    self.autosave_filename = output_filename + '.autosave'

    if use_config is not None:
      self.config = use_config
    else:
      self.config = BigQuerierConfig()

  def _detect_missing_query_terms(self):
    missing_count = 0
    for input_object in self._input_data:
      try:
        input_object[keys.QUERY_TERM]
      except KeyError:
        missing_count = missing_count + 1
        continue
    
    self.missing_count = missing_count
    if self.missing_count > 0:
      logger.warning(
        f'Found {str(self.missing_count)} entry(s) with missing query term, '
        f'which will be skipped'
      )

  def begin(
    self,
    webdriver: WebDriver,
    keyword: str,
    *,
    query_depth=1,
    query_lang='id',
    autosave_every=1
  ):
    logger.info(
      f'Starting big query of "{self.source_filename}", keyword: "{keyword}"'
    )

    queries_data = processing.preproc_queries(
      keyword, self._input_data
    )

    self.webdriver = webdriver
    self.querier = Querier(
      self.webdriver,
      loading_timeout_seconds=self.config.loading_timeout_seconds,
      scroll_wait_seconds=self.config.scroll_wait_seconds,
      scroll_retries=self.config.scroll_retries
    )

    for index, query_object in enumerate(queries_data):
      try:
        query = query_object[keys.QUERY]
      except KeyError:
        self.missing_data.append(query_object)
        logger.info(
          f'({str(index+1)}/{str(self.queries_count)}): Skipping due to missing query term'
        )
        logger.debug(
          f'Missing query-term object:\n{str(query_object)}'
        )
        continue
      
      logger.info(
        f'({str(index+1)}/{str(self.queries_count)}): Querying "{query}"'
      )

      output_object = query_object.copy()
      try:
        results = self._begin_one(
          query,
          query_depth=query_depth,
          query_lang=query_lang
        )

      except Exception as e:
        self.errored_count = self.errored_count + 1
        self.errored_data.append(query_object)

        logger.error(str(e))
        logger.error(
          f'Could not process entry #{str(index+1)}'
        )
        logger.debug(
          f'Errored object:\n{str(query_object)}'
        )
        continue

      output_object.update(results)
      self._output_data.append(output_object)
      self.outputs_count = len(self._output_data)
      self.autosave(autosave_every)
    
    logger.info(
      f'Finished big query of "{self.source_filename}"'
    )
    logger.info(
      f'{str(self.queries_count)} input entries, '
      f'{str(self.outputs_count)} result(s), '
      f'{str(self.missing_count)} missing(s), '
      f'{str(self.errored_count)} error(s)'
    )
    if len(self.missing_data) > 0:
      logger.debug(
        f'The following object(s) have missing query item:\n' +
        '\n'.join(
          [str(missing_object) for missing_object in self.missing_data]
        )
      )
    if len(self.errored_data) > 0:
      logger.debug(
        f'The following object(s) outputed errors:\n' +
        '\n'.join(
          [str(errored_object) for errored_object in self.errored_data]
        )
      )

  def _begin_one(self,
    query: str,
    *,
    query_depth=1,
    query_lang='id'
  ):
    self.querier.begin(query, query_depth=query_depth, query_lang=query_lang)

    result = self.querier.grab_results()
    return result.report()
  
  def postprocess(self):
    self._output_data = processing.postproc_queries(self._output_data)

  def autosave(
    self,
    every: int
  ):    
    if self.outputs_count % every == 0:
      try:
        with open(self.autosave_filename, 'w', encoding='UTF-8') as json_file:
          json.dump(self.output_data, json_file, indent=1)
      except OSError as e:
        logger.error(str(e))
        logger.error(
          f'Unable to autosave to "{self.autosave_filename}"'
        )
      else:
        logger.info(
          f'Autosaved to "{self.autosave_filename}"'
        )
  
  def export_json(
    self,
    filename=None,
    indent=1
  ):
    if filename is None:
      filename = self.output_filename

    try:
      with open(filename, 'w', encoding='UTF-8') as json_file:
        json.dump(self.output_data, json_file, indent=indent)
    except OSError as e:
      logger.error(str(e))
      logger.error(
        f'Unable to export to JSON file {filename}'
      )
      return
    
    logger.info(
      f'Exported data to JSON file "{filename}"'
    )

    try:
      os.remove(self.autosave_filename)
    except OSError:
      pass
    else:
      logger.info(
        f'Removed autosave "{self.autosave_filename}"'
      )


  @property
  def input_data(self):
    return self._input_data
  
  @property
  def output_data(self):
    return self._output_data
  
  @property
  def INFINITE_SCROLL(self):
      return 0