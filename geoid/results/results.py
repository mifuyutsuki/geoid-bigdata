from copy import deepcopy
import csv, json, logging

from geoid.constants import keys
from .metadata import Metadata
from . import parsing

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

class Results:
  def __init__(self):
    self.metadata       = Metadata('', '', 0)
    self._results       = []
    self._results_count = 0
  
  def from_html(
    self,
    grabbed_html: str
  ):
    logger.info(
      f'Processing results of query: "{self.metadata.query}"'
    )
    
    #: 1. Parse (before municipality data)
    results = parsing.parse_html(grabbed_html, self.metadata)
    
    #: 2. Get municipality data
    logger.info(
      f'Getting municipality data: "{self.metadata.query}"'
    )
    results, errors = parsing.get_municipality_data(results)
    
    if errors > 0:     
      logger.warning(
        f'Could not pull municipality data of {str(errors)} entry(s)'
      )

    #: Finalize
    self._results = results
    self._results_count = len(results)

    logger.info(
      f'Processed results of query: "{self.metadata.query}"'
    )

    return self
    
  # def export_csv(
  #   self,
  #   filename: str,
  #   *,
  #   quoting=csv.QUOTE_ALL,
  #   lineterminator='\n',
  #   **csv_kwargs
  # ):
  #   if len(self.results) <= 0:
  #     raise ValueError('No search results entries to export')
  #   if len(filename) <= 0:
  #     raise ValueError('Filename cannot be blank')
    
  #   # Fields with newlines cause issues in CSV
  #   results = deepcopy(self.results)
  #   for result in results:
  #     for value in result.values():
  #       value = value.replace('\n', '; ')
    
  #   with open(filename, 'w', encoding='UTF-8') as csv_file:
  #     csv_writer = csv.DictWriter(
  #       csv_file,
  #       fieldnames=self._keys,
  #       quoting=quoting,
  #       lineterminator=lineterminator,
  #       **csv_kwargs
  #     )
  #     csv_writer.writeheader()
  #     csv_writer.writerows(results)

  #   logger.info(
  #     f'Exported query to CSV file "{filename}"'
  #   )
  
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
      keys.QUERY               : self.metadata.query,
      keys.QUERY_LANG          : self.metadata.lang,
      keys.QUERY_TIMESTAMP     : self.metadata.timestamp,
      keys.QUERY_RESULTS_COUNT : self.results_count,
      keys.QUERY_RESULTS       : self.results
    }

    logger.debug(
      f'Generated query report of "{self.metadata.query}"'
    )
    return deepcopy(report_dump)

  def results_copy(self):
    return deepcopy(self._results)
  
  #: Properties are read-only
  
  @property
  def results(self) -> list[dict]:
    return self._results
  
  @property
  def results_count(self) -> int:
    return self._results_count