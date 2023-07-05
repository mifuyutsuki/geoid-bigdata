from copy import deepcopy
import csv, json, logging

from geoid.constants import Keys
from .metadata import Metadata


logger = logging.getLogger(__name__)


class Results:
  def __init__(self):
    self.metadata = Metadata()
    self.results  = []
    self.count    = 0
    
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
      Keys.QUERY               : self.metadata.query,
      Keys.QUERY_LANG          : self.metadata.lang,
      Keys.QUERY_TIMESTAMP     : self.metadata.timestamp,
      Keys.QUERY_STATUS        : self.metadata.status,
      Keys.QUERY_RESULTS_COUNT : self.count,
      Keys.QUERY_RESULTS       : self.results
    }

    logger.debug(
      f'Generated query report of "{self.metadata.query}"'
    )
    return deepcopy(report_dump)

  def results_copy(self):
    return deepcopy(self._results)