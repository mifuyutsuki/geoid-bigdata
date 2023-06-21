from selenium.common.exceptions import *
from selenium.webdriver.remote.webdriver import WebDriver
from copy import deepcopy
import json, logging

from .querier import Querier

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
class BigQuerier:
  def __init__(
    self,
    webdriver: WebDriver,
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

    self.logger = logging.getLogger(__name__)
    self.logger.info(
      f'Imported queries file "{source_json_file}"'
    )

    queries_count = self._count_queries()
    self.logger.info(
      f'Found {str(queries_count)} query object(s)'
    )

    self.webdriver = webdriver
    self.querier   = None
    
    self.source_file             = source_json_file
    self.loading_timeout_seconds = loading_timeout_seconds
    self.scroll_wait_seconds     = scroll_wait_seconds
    self.scroll_retries          = scroll_retries
  
  def _preprocess_query(
    self,
    keyword: str
  ):
    for input_object in self._input_data:
      input_object['query'] = f"{keyword} {input_object['nama_kabupaten_kota']}"

  def begin(
    self,
    *,
    keyword=None,
    query_depth=1,
    query_language='id'
  ):
    if type(keyword) is str:
      self._preprocess_query(keyword)
    elif keyword is None:
      self._check_query_fields()
    else:
      raise ValueError(f'Invalid query keyword of type "{type(keyword).__name__}"')

    self.logger.info(
      f'Starting big query of "{self.source_file}", keyword: "{keyword}"'
    )

    self.querier = Querier(
      self.webdriver,
      loading_timeout_seconds=self.loading_timeout_seconds,
      scroll_wait_seconds=self.scroll_wait_seconds,
      scroll_retries=self.scroll_retries
    )

    for input_object in self.input_data:
      output_object = input_object.copy()
      results = self._begin_one(
        input_object,
        query_depth=query_depth,
        query_language=query_language
      )
      output_object.update(results)
      self._output_data.append(output_object)
    
    self.logger.info(
      f'Finished big query of "{self.source_file}"'
    )
  
  def postprocess(self):
    unprocessed_data  = self.output_data.copy()
    filtered_data     = self._postprocess_filter(unprocessed_data)
    flattened_data    = self._postprocess_flatten(filtered_data)
    self._output_data = flattened_data
  
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
        query_city = query_result['kab_kota']
        if (
          target_city.strip().lower() == query_city.strip().lower()
        ):
          filtered_query_results.append(query_result.copy())
        else:
          filtered_count = filtered_count + 1
        
      query_object['query_results'] = filtered_query_results
      query_object['query_results_count'] = len(filtered_query_results)

    self.logger.info(
      f'Postprocessing - removed {str(filtered_count)} result(s)' + \
      ' with mismatched location'
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
          if key.lower() in ('provinsi', 'kab_kota'):
            continue
          result_object[key] = query_result[key]
        flattened_object = head_object.copy()
        flattened_object.update(result_object)
        flattened_data.append(flattened_object)
    
    self.logger.info(
      'Postprocessing - flattened query results'
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
    
    self.logger.info(
      f'Exported big query to JSON file "{filename}"'
    )

  def _begin_one(self,
    query_object: dict,
    *,
    query_depth=1,
    query_language='id'
  ):
    try:
      query = query_object['query']
    except KeyError:
      return
    
    self.querier.begin(query, query_depth=query_depth, query_language=query_language)
    result = self.querier.grab_results()
    return result.report()
  
  def _count_queries(self) -> int:
    return len(self._input_data)

  def _check_query_fields(self):
    for index, data in enumerate(self.input_data):
      try:
        data['query']
      except KeyError:
        self.logger.warning(
          f'Input entry #{str(index+1)} is missing a query - skipping'
        )
  
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