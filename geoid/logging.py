import time, os, logging.config

#: Logging configuration is set this way (as .py) due to the need to grab
#: datetime information for the log file name.

LOG_FORMAT = '[%(asctime)s] [%(name)s:%(lineno)s] %(levelname)s: %(message)s'
LOG_DATETIME = time.strftime('%Y%m%d_%H%M%S')
LOG_FILENAME = r'logs\{0}.log'.format(LOG_DATETIME)

#: Using DEBUG induces logging errors due to selenium logging the HTML, which
#: contains special Unicode characters. (The program can continue, though.)

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
      'level': 'WARNING',
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


LOG_CONFIG_INFO = LOG_CONFIG_STD.copy()
LOG_CONFIG_INFO.update({
  'handlers': {
    'console': {
      'level': 'INFO'
    }
  }
})


def _check_folder():
  if not os.path.exists(r'./logs/'):
    os.mkdir(r'./logs/')


def log_start(show_info=False):
  if show_info:
    log_info()
  else:
    log_std()


def log_std():
  """
  Start logging with level WARNING on stdout and INFO file.
  """

  _check_folder()
  logging.config.dictConfig(LOG_CONFIG_STD)


def log_info():
  """
  Start logging with level INFO on both stdout and file.
  """

  _check_folder()
  logging.config.dictConfig(LOG_CONFIG_INFO)
  