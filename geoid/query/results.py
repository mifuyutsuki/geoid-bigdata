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
    

  def from_query_object(self, data_object: dict):
    self.metadata.status    = data_object[Keys.QUERY_STATUS]
    self.metadata.query     = data_object[Keys.QUERY_KEYWORD]
    self.metadata.lang      = data_object[Keys.QUERY_LANG]
    self.metadata.timestamp = data_object[Keys.QUERY_TIMESTAMP]
    self.results            = data_object[Keys.QUERY_RESULTS]
    self.count              = data_object[Keys.QUERY_RESULTS_COUNT]

  
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
      Keys.QUERY_KEYWORD       : self.metadata.query,
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