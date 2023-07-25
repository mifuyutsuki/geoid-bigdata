from .keys import Keys
from .status import Status

class Objects:
  BASE_QUERY_OBJECT = {
    Keys.QUERY_TERM          : None,
    Keys.QUERY_LOCATION      : None,
    Keys.QUERY_KEYWORD       : None,
    Keys.QUERY_LANG          : None,
    Keys.QUERY_TIMESTAMP     : 0,
    Keys.QUERY_STATUS        : Status.QUERY_INCOMPLETE,
    Keys.QUERY_RESULTS_COUNT : 0,
    Keys.QUERY_RESULTS       : []
  }

  BASE_PLACE_OBJECT = {
    Keys.LOCATION_NAME : None,
    Keys.LOCATION_TYPE : None,
    Keys.LATITUDE      : None,
    Keys.LONGITUDE     : None,
    Keys.PROVINCE_ID   : None,
    Keys.PROVINCE_NAME : None,
    Keys.CITY_ID       : None,
    Keys.CITY_NAME     : None,
    Keys.DISTRICT_ID   : None,
    Keys.DISTRICT_NAME : None,
    Keys.VILLAGE_ID    : None,
    Keys.VILLAGE_NAME  : None,
    Keys.POSTAL_CODE   : None,
    Keys.RATING        : None,
    Keys.REVIEWS       : None,
    Keys.DESCRIPTION   : None,
    Keys.LOCATION_LINK : None
  }