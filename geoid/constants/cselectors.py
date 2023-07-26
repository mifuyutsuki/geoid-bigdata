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

#: Some class names in GMaps do contain trailing whitespaces.

class Selectors:
  #: Elements CSS selectors
  TARGET_RESULT       = 'div[class="Nv2PK THOPZb CpccDe "]'
  GENERAL_RESULT      = '.Nv2PK'
  RESULT              = '.Nv2PK'
  RESULTS_BOX         = '.DxyBCb'
  RESULTS_BOTTOM      = '.lXJj5c'
  RESULTS_END         = '.eKbjU'
  SEARCHBOX           = '#searchbox'

  #: Field CSS selectors
  LOCATION_NAME_FIELD = '.qBF1Pd'
  LOCATION_TYPE_FIELD = '.W4Efsd.W4Efsd>span>span'
  LATITUDE_FIELD      = 'a[href]'
  LONGITUDE_FIELD     = 'a[href]'
  RATING_FIELD        = '.MW4etd'
  REVIEWS_FIELD       = '.UY7F9'
  DESCRIPTION_FIELD   = '.W4Efsd.W4Efsd'
  LOCATION_LINK_FIELD = 'a[href]'
  IMAGE_LINK_FIELD    = 'img[src]'

  #: Other selectors
  RECAPTCHA           = 'iframe[src][title="reCAPTCHA"]'