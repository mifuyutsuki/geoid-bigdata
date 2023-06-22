from selenium.common.exceptions import *
from selenium.webdriver.remote.webdriver import WebDriver
from copy import deepcopy
import json, logging

from .querier import Querier

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

class BigQuerier:
  def __init__(
    self,
    source_json_file: str,
    *,
    loading_timeout_seconds=15.0,
    scroll_wait_seconds=2.5,
    scroll_retries=5
  ):
    self._output_data = []
    with open(source_json_file, 'r', encoding='UTF-8') as json_file:
      self._input_data = json.load(json_file)
    
    if type(self._input_data) is not list:
      raise ValueError(f'Query file "{source_json_file}" must be an array of objects')

    logger.info(
      f'Imported queries file "{source_json_file}"'
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
    
    self.source_file             = source_json_file
    self.loading_timeout_seconds = loading_timeout_seconds
    self.scroll_wait_seconds     = scroll_wait_seconds
    self.scroll_retries          = scroll_retries

  def begin(
    self,
    webdriver: WebDriver,
    keyword: str,
    *,
    query_depth=1,
    query_language='id'
  ):
    logger.info(
      f'Starting big query of "{self.source_file}", keyword: "{keyword}"'
    )

    self._preprocess_query(keyword)

    self.webdriver = webdriver
    self.querier = Querier(
      self.webdriver,
      loading_timeout_seconds=self.loading_timeout_seconds,
      scroll_wait_seconds=self.scroll_wait_seconds,
      scroll_retries=self.scroll_retries
    )

    for index, input_object in enumerate(self.input_data):
      try:
        query = input_object['query']
      except KeyError:
        self.missing_data.append(input_object)
        logger.info(
          f'({str(index+1)}/{str(self.queries_count)}): Skipping due to missing query term'
        )
        logger.debug(
          f'Missing query-term object:\n{str(input_object)}'
        )
        continue
      
      logger.info(
        f'({str(index+1)}/{str(self.queries_count)}): Querying "{query}"'
      )

      output_object = input_object.copy()
      try:
        results = self._begin_one(
          query,
          query_depth=query_depth,
          query_language=query_language
        )

      except NoSuchElementException:
        # This is typically called by the missing results-box
        self.errored_count = self.errored_count + 1
        self.errored_data.append(input_object)

        logger.error(
          f'Could not process entry #{str(index+1)}'
        )
        logger.debug(
          f'Errored object:\n{str(input_object)}'
        )
        continue

      except Exception as e:
        self.errored_count = self.errored_count + 1
        self.errored_data.append(input_object)

        logger.exception(e)
        logger.error(
          f'Could not process entry #{str(index+1)}'
        )
        logger.debug(
          f'Errored object:\n{str(input_object)}'
        )
        continue

      output_object.update(results)
      self._output_data.append(output_object)
    
    self.outputs_count = len(self._output_data)
    logger.info(
      f'Finished big query of "{self.source_file}"'
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
  
  def _detect_missing_query_terms(self):
    missing_count = 0
    for input_object in self._input_data:
      try:
        input_object['query_term']
      except KeyError:
        missing_count = missing_count + 1
        continue
    
    self.missing_count = missing_count
    if self.missing_count > 0:
      logger.warning(
        f'Found {str(self.missing_count)} entry(s) with missing query term, '
        f'which will be skipped'
      )
  
  def _preprocess_query(
    self,
    keyword: str
  ):
    for input_object in self._input_data:
      try:
        input_object['query_term']
      except KeyError:
        continue

      input_object['query'] = f"{keyword} {input_object['query_term']}"
  
  def postprocess(self):
    unprocessed_data  = self.output_data.copy()
    filtered_data     = self._postprocess_filter(unprocessed_data)
    flattened_data    = self._postprocess_flatten(filtered_data)
    self._output_data = flattened_data

    objects_count_after = len(self.output_data)
    logger.info(
      f'Postprocessing - {str(objects_count_after)} entry(s)'
    )
  
  def _postprocess_filter(
    self,
    data: list[dict]
  ) -> list[dict]:
    filtered_data = data
    filtered_count = 0
    for query_object in filtered_data:
      try:
        target_city   = query_object['nama_kabupaten_kota']
        query_results = query_object['query_results']
      except KeyError:
        continue
      
      filtered_query_results = []
      for query_result in query_results:
        query_city = query_result['nama_kabupaten_kota']
        if (
          target_city.strip().lower() == query_city.strip().lower()
        ):
          filtered_query_results.append(query_result.copy())
        else:
          filtered_count = filtered_count + 1
        
      query_object['query_results'] = filtered_query_results
      query_object['query_results_count'] = len(filtered_query_results)

    logger.info(
      f'Postprocessing - removed {str(filtered_count)} result(s) '
      f'with mismatched location'
    )
    return filtered_data
  
  def _postprocess_flatten(
    self,
    data: list[dict]
  ) -> list[dict]:
    flattened_data = []
    for query_object in data:
      try:
        query_results = query_object['query_results']
      except KeyError:
        continue
      
      head_object = dict()
      for key in query_object.keys():
        #: Exclude keys
        if key.lower() in ('query_results', 'query_results_count'):
          continue
        head_object[key] = query_object[key]

      for query_result in query_results:
        result_object = dict()
        for key in query_result.keys():
          #: Exclude keys
          if key.lower() in ('nama_provinsi', 'nama_kabupaten_kota'):
            continue
          result_object[key] = query_result[key]
        flattened_object = head_object.copy()
        flattened_object.update(result_object)
        flattened_data.append(flattened_object)
    
    logger.info(
      f'Postprocessing - flattened query results'
    )
    return flattened_data

  def export_json(
    self,
    filename: str,
    indent=1
  ):
    if len(filename) <= 0:
      raise ValueError('Filename must not be empty')

    with open(filename, 'w', encoding='UTF-8') as json_file:
      json.dump(self.output_data, json_file, indent=indent)
    
    logger.info(
      f'Exported big query to JSON file "{filename}"'
    )

  def _begin_one(self,
    query: str,
    *,
    query_depth=1,
    query_language='id'
  ):
    self.querier.begin(query, query_depth=query_depth, query_language=query_language)

    result = self.querier.grab_results()
    return result.report()
  
  def input_data_copy(self):
    return deepcopy(self._input_data)
  
  def output_data_copy(self):
    return deepcopy(self._output_data)

  @property
  def input_data(self):
    return self._input_data
  
  @property
  def output_data(self):
    return self._output_data
  
  @property
  def INFINITE_SCROLL(self):
      return 0