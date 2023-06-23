import time

#: Logging configuration is set this way (as .py) due to the need to grab
#: datetime information for the log file name.

LOG_FORMAT = '[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
LOG_DATETIME = time.strftime('%Y%m%d_%H%M%S')
LOG_FILENAME = r'logs\{0}.log'.format(LOG_DATETIME)

#: Using DEBUG induces logging errors due to selenium logging the HTML, which
#: contains special Unicode characters. (The program can continue, though.)

LOG_CONFIG = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "std": {
      "format": LOG_FORMAT
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "stream": "ext://sys.stdout",
      "level": "INFO",
      "formatter": "std"
    },
    "file": {
      "class": "logging.FileHandler",
      "filename": LOG_FILENAME,
      "mode": "w",
      "level": "INFO",
      "formatter": "std"
    }
  },
  "root": {
    "level": "INFO",
    "handlers": ["console", "file"]        
  }
}