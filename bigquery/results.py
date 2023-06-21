from bs4 import BeautifulSoup, Tag
from urllib.parse import quote_plus
from copy import deepcopy
import requests
import csv, json, re, logging

logging.basicConfig(
  level=logging.INFO,
  format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

class Results:
  def __init_selectors(self):
    #: Some class names do contain trailing whitespaces; however,
    #: class trailing whitespaces in the HTML fed to bs4 are removed
    self.__RESULT_SELECTOR              = 'div[class="Nv2PK THOPZb CpccDe"]'
    self.__LOCATION_NAME_FIELD_SELECTOR = 'div[class="qBF1Pd fontHeadlineSmall"]'
    self.__LOCATION_TYPE_FIELD_SELECTOR = 'div[class="W4Efsd"] > div[class="W4Efsd"] > span > span'
    self.__LATITUDE_FIELD_SELECTOR      = 'a[href]'
    self.__LONGITUDE_FIELD_SELECTOR     = 'a[href]'
    self.__RATING_FIELD_SELECTOR        = 'span[class="MW4etd"]'
    self.__REVIEWS_FIELD_SELECTOR       = 'span[class="UY7F9"]'
    self.__DESCRIPTION_FIELD_SELECTOR   = 'div[class="W4Efsd"] > div[class="W4Efsd"]'
    self.__LOCATION_LINK_FIELD_SELECTOR = 'a[href]'
    self.__IMAGE_LINK_FIELD_SELECTOR    = 'img[src]'

  def __init__(
    self,
    grabbed_html: str,
    query: str,
    query_language: str,
    query_timestamp: int
  ):
    self.__init_selectors()
    self._query = query
    self._query_language = query_language
    self._query_timestamp = query_timestamp

    logger = logging.getLogger(__name__)

    results = []

    logger.info(
      f'Processing results of query: "{self._query}"'
    )

    #: 1. Parse
    dump_soup = BeautifulSoup(grabbed_html, 'lxml')
    entries = dump_soup.select(self.__RESULT_SELECTOR)

    for entry in entries:
      if entry is not None:
        result = self._process_entry(entry)
        results.append(result)
    
    #: 2. Get Subdivision
    logger.info(
      f'Getting municipality data: "{self._query}"'
    )
    process_error_count = 0
    for result in results:
      try:
        result = self._process_fields_municipality(result)
      except (KeyError, requests.HTTPError):
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
    quoting=csv.QUOTE_ALL,
    lineterminator='\n'
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
      csv_writer = csv.DictWriter( \
        csv_file, fieldnames=self._keys, \
        quoting=quoting, lineterminator=lineterminator
      )
      csv_writer.writeheader()
      csv_writer.writerows(results)

    logger.info(
      f'Exported query to CSV file "{filename}"'
    )
  
  def export_json(self, filename: str, indent=1) -> None:
    if len(self.results) <= 0:
      raise ValueError('No search results entries to export')
    if len(filename) <= 0:
      raise ValueError('Filename must not be empty')
  
    json_dump = self.report()
    
    with open(filename, 'w', encoding='UTF-8') as json_file:
      json.dump(json_dump, json_file, indent=indent)
    logger.info(
      f'Exported query to JSON file "{filename}"'
    )

  def report(self) -> dict:
    report_dump = {
      'query'               : self.query,
      'query_language'      : self.query_language,
      'query_timestamp'     : self.query_timestamp,
      'query_results_count' : self.results_count,
      'query_results'       : self.results
    }
    logger.debug(
      f'Generated query report of "{self.query}"'
    )
    return deepcopy(report_dump)
  
  # Internal use functions below

  def _get_municipality(self, latitude, longitude):
    request = requests.get(
      f'https://kodeposku.com/api/nearest?lat={str(latitude)}&lon={str(longitude)}'
    )
    request.raise_for_status()
    return request.json()
  
  def _process_fields_municipality(self, result_entry):
    municipality_fields = self._get_municipality(
        result_entry['latitude'], result_entry['longitude']
    )
    result_entry['provinsi']     = \
      str(municipality_fields['province'])
    result_entry['kab_kota']     = \
      str(municipality_fields['city'])
    result_entry['id_kecamatan'] = \
      self._process_field_id_district(municipality_fields['code'])
    result_entry['kecamatan']    = \
      str(municipality_fields['district'])
    result_entry['id_kel_desa']  = \
      self._process_field_id_village(municipality_fields['code'])
    result_entry['kel_desa']     = \
      str(municipality_fields['village'])
    result_entry['kode_pos']     = \
      str(municipality_fields['postal'])
    return result_entry

  def _process_field_id_district(self, code) -> str:
    subcodes = re.findall(r'[0-9]+', code)
    try:
      field  = ''.join(subcodes[0:3])
    except IndexError:
      field  = ''
    return field

  def _process_field_id_village(self, code) -> str:
    subcodes = re.findall(r'[0-9]+', code)
    try:
      field  = ''.join(subcodes)
    except IndexError:
      field  = ''
    return field

  def _process_entry(self, entry: Tag) -> dict:
    result_entry = dict()
    result_entry['location_name'] = self._process_field_location_name(entry)
    result_entry['location_type'] = self._process_field_location_type(entry)
    result_entry['latitude']      = self._process_field_latitude(entry) 
    result_entry['longitude']     = self._process_field_longitude(entry)

    #: These fields are filled in another process function
    result_entry['provinsi']      = ''
    result_entry['kab_kota']      = ''
    result_entry['id_kecamatan']  = ''
    result_entry['kecamatan']     = ''
    result_entry['id_kel_desa']   = ''
    result_entry['kel_desa']      = ''
    result_entry['kode_pos']      = ''

    result_entry['rating']        = self._process_field_rating(entry)
    result_entry['reviews']       = self._process_field_reviews(entry)
    result_entry['description']   = self._process_field_description(entry)
    result_entry['location_link'] = self._process_field_location_link(entry)
    result_entry['image_link']    = self._process_field_image_link(entry)
    self._keys = result_entry.keys()
    return result_entry
  
  def _process_field_location_name(self, entry: Tag) -> str:
    field_selection = entry.select_one(self.__LOCATION_NAME_FIELD_SELECTOR)
    if field_selection is not None:
      field = field_selection.string
    else:
      field = ''
    return field
  
  def _process_field_location_type(self, entry: Tag) -> str:
    field_selection = entry.select_one(self.__LOCATION_TYPE_FIELD_SELECTOR)
    if field_selection is not None:
      field = field_selection.string
    else:
      field = ''
    return field
      
  def _process_field_latitude(self, entry: Tag) -> str:
    field_selection = entry.select_one(self.__LATITUDE_FIELD_SELECTOR)
    if field_selection is not None:
      field = field_selection['href']
    else:
      field = ''
    
    field_regex = re.search(r'(?<=!3d)-?[0-9]+[.,].[0-9]+', field)
    if field_regex is not None:
      field = field_regex.group(0)
    return field
      
  def _process_field_longitude(self, entry: Tag) -> str:
    field_selection = entry.select_one(self.__LONGITUDE_FIELD_SELECTOR)
    if field_selection is not None:
      field = field_selection['href']
    else:
      field = ''
    
    field_regex = re.search(r'(?<=!4d)-?[0-9]+[.,].[0-9]+', field)
    if field_regex is not None:
      field = field_regex.group(0)
    return field

  def _process_field_rating(self, entry: Tag) -> str:
    # Rating is of the form 4.8 or 4,8
    # -> Account for decimal comma
    field_selection = entry.select_one(self.__RATING_FIELD_SELECTOR)
    if field_selection is not None:
      field = field_selection.string
      field = field.replace(',', '.')
    else:
      field = ''
    return field
  
  def _process_field_reviews(self, entry: Tag) -> str:
    # Review count is of the form (11,111) or (11.111)
    # -> Ignore non-numbers
    field_selection = entry.select_one(self.__REVIEWS_FIELD_SELECTOR)
    if field_selection is not None:
      field = field_selection.string
      field = re.sub('[^0-9]', '', field)
    else:
      field = ''
    return field
  
  def _process_field_description(self, entry: Tag) -> str:
    #: Description is of the form [" ", " ", " ", " "]
    #: -> Join same-line blocks with whitespace
    #: -> Join different lines with newline
    field_selections = entry.select(self.__DESCRIPTION_FIELD_SELECTOR)
    field_lines = []
    for index, selection in enumerate(field_selections):
      #: Skip the first field, as it is already processed as location type 
      if index == 0:
        continue
      field_lines.append(' '.join(list(selection.stripped_strings)))
    field = '\n'.join(field_lines)
    return field
  
  def _process_field_location_link(self, entry: Tag) -> str:
    #: The section after '?' grabbed from the fields can be dropped
    #: However, keep the host query_language query (from caller)
    field_selection = entry.select_one(self.__LOCATION_LINK_FIELD_SELECTOR)
    if field_selection is not None:
      field = field_selection['href'].rsplit('?')[0] + f'?hl={quote_plus(self.query_language)}'
    else:
      field = ''
    return field
  
  def _process_field_image_link(self, entry: Tag) -> str:
    # Stripping the section after '=' yields the original size img
    field_selection = entry.select_one(self.__IMAGE_LINK_FIELD_SELECTOR)
    if field_selection is not None:
      field = field_selection['src'].rsplit('=')[0]
    else:
      field = ''
    return field

  def results_copy(self):
    return deepcopy(self._results)
  
  #: Properties are read-only

  @property
  def query(self) -> str:
    return self._query
  
  @property
  def query_language(self) -> str:
    return self._query_language
  
  @property
  def query_timestamp(self) -> int:
    return self._query_timestamp
  
  @property
  def results(self) -> list[dict]:
    return self._results
  
  @property
  def results_count(self) -> int:
    return self._results_count
  