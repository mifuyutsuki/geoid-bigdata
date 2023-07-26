# Copyright (c) 2023 mifuyutsuki

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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