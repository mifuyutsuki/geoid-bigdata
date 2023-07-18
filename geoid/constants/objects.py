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