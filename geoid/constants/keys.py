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

class Keys:
  #: Field keys
  LOCATION_NAME = 'location_name'
  LOCATION_TYPE = 'location_type'
  LATITUDE      = 'latitude'
  LONGITUDE     = 'longitude'
  PROVINCE_ID   = 'id_provinsi'
  PROVINCE_NAME = 'nama_provinsi'
  CITY_ID       = 'id_kabupaten_kota'
  CITY_NAME     = 'nama_kabupaten_kota'
  DISTRICT_ID   = 'id_kecamatan'
  DISTRICT_NAME = 'nama_kecamatan'
  VILLAGE_ID    = 'id_kelurahan_desa'
  VILLAGE_NAME  = 'nama_kelurahan_desa'
  POSTAL_CODE   = 'kode_pos'
  RATING        = 'rating'
  REVIEWS       = 'reviews'
  DESCRIPTION   = 'description'
  LOCATION_LINK = 'location_link'
  IMAGE_LINK    = 'image_link'

  #: Query results keys
  QUERY_TERM          = 'query_term'
  QUERY_LOCATION      = 'query_location'
  QUERY_KEYWORD       = 'query_keyword'
  QUERY_LANG          = 'query_lang'
  QUERY_TIMESTAMP     = 'query_timestamp'
  QUERY_STATUS        = 'query_status'
  QUERY_RESULTS_COUNT = 'query_results_count'
  QUERY_RESULTS       = 'query_results'

  #: Query status report keys
  REPORT_NO     = 'no'
  REPORT_QUERY  = 'query'
  REPORT_STATUS = 'status'