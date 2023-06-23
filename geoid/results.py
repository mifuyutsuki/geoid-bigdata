from bs4 import BeautifulSoup
from copy import deepcopy
import csv, json, logging

from .constants import cselectors, keys
from . import processing

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger('Results')

class Results:
  def __init__(
    self,
    grabbed_html: str,
    query: str,
    query_lang: str,
    query_timestamp: int
  ):
    self._keys = None
    self._query = query
    self._query_lang = query_lang
    self._query_timestamp = query_timestamp

    results = []

    logger.info(
      f'Processing results of query: "{self._query}"'
    )

    #: 1. Parse
    dump_soup = BeautifulSoup(grabbed_html, 'lxml')
    results_raw = dump_soup.select(cselectors.RESULT)

    for result_raw in results_raw:
      if result_raw is not None:
        result = processing.results.proc_entry(
          result_raw, query_lang=query_lang
        )
        results.append(result)
    
    #: 2. Get Subdivision
    logger.info(
      f'Getting municipality data: "{self._query}"'
    )
    process_error_count = 0
    for result in results:
      try:
        result = processing.results.proc_municipality(result)
      except Exception as e:
        logger.error(str(e))
        process_error_count = process_error_count + 1
        continue
    
    logger.info(
      f'Got municipality data: "{self._query}"'
    )
    if process_error_count > 0:     
      logger.warning(
        f'Could not pull municipality data of {process_error_count} entry(s)'
      )

    #: Finalize
    self._results = results
    self._results_count = len(results)

    logger.info(
      f'Processed results of query: "{self._query}"'
    )
  
  def export_csv(
    self,
    filename: str,
    *,
    quoting=csv.QUOTE_ALL,
    lineterminator='\n',
    **csv_kwargs
  ):
    if len(self.results) <= 0:
      raise ValueError('No search results entries to export')
    if len(filename) <= 0:
      raise ValueError('Filename cannot be blank')
    
    # Fields with newlines cause issues in CSV
    results = deepcopy(self.results)
    for result in results:
      for key in result.keys():
        result[key] = result[key].replace('\n', '; ')
    
    with open(filename, 'w', encoding='UTF-8') as csv_file:
      csv_writer = csv.DictWriter(
        csv_file,
        fieldnames=self._keys,
        quoting=quoting,
        lineterminator=lineterminator,
        **csv_kwargs
      )
      csv_writer.writeheader()
      csv_writer.writerows(results)

    logger.info(
      f'Exported query to CSV file "{filename}"'
    )
  
  def export_json(
    self,
    filename: str,
    *,
    indent=1,
    **json_kwargs
  ):
    if len(self.results) <= 0:
      raise ValueError('No search results entries to export')
    if len(filename) <= 0:
      raise ValueError('Filename must not be empty')
  
    json_dump = self.report()
    
    with open(filename, 'w', encoding='UTF-8') as json_file:
      json.dump(json_dump, json_file, indent=indent, **json_kwargs)
    logger.info(
      f'Exported query to JSON file "{filename}"'
    )

  def report(self) -> dict:
    report_dump = {
      keys.QUERY               : self.query,
      keys.QUERY_LANG          : self.query_lang,
      keys.QUERY_TIMESTAMP     : self.query_timestamp,
      keys.QUERY_RESULTS_COUNT : self.results_count,
      keys.QUERY_RESULTS       : self.results
    }

    logger.debug(
      f'Generated query report of "{self.query}"'
    )
    return deepcopy(report_dump)

  def results_copy(self):
    return deepcopy(self._results)
  
  #: Properties are read-only

  @property
  def query(self) -> str:
    return self._query
  
  @property
  def query_lang(self) -> str:
    return self._query_lang
  
  @property
  def query_timestamp(self) -> int:
    return self._query_timestamp
  
  @property
  def results(self) -> list[dict]:
    return self._results
  
  @property
  def results_count(self) -> int:
    return self._results_count