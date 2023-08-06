# Copyright (c) 2023 Mifuyu (mifuyutsuki@proton.me)

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

import time, os, logging.config

#: Logging configuration is set this way (as .py) due to the need to grab
#: datetime information for the log file name.

LOG_FORMAT = '[%(asctime)s] [%(name)s:%(lineno)s] %(levelname)s: %(message)s'
LOG_DATETIME = time.strftime('%Y%m%d_%H%M%S')
LOG_FILENAME = r'logs\{0}.log'.format(LOG_DATETIME)

#: Using DEBUG induces logging errors due to selenium logging the HTML, which
#: may contain special Unicode characters. (The program can continue, though.)

LOG_CONFIG_STD = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'std': {
      'format': LOG_FORMAT
    }
  },
  'handlers': {
    'console': {
      'class': 'logging.StreamHandler',
      'stream': 'ext://sys.stdout',
      'level': 'INFO',
      'formatter': 'std'
    },
    'file': {
      'class': 'logging.FileHandler',
      'filename': LOG_FILENAME,
      'mode': 'w',
      'level': 'INFO',
      'formatter': 'std'
    }
  },
  'root': {
    'level': 'INFO',
    'handlers': ['console', 'file']        
  }
}


def _check_folder():
  if not os.path.exists(r'./logs/'):
    os.mkdir(r'./logs/')


def log_start():
  _check_folder()
  logging.config.dictConfig(LOG_CONFIG_STD)
  