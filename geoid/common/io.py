import os, json, logging


logger = logging.getLogger(__name__)


def import_json(filename: str):
  with open(filename, 'r', encoding='UTF-8') as json_file:
    data = json.load(json_file)
  
  logger.info(
    f'Imported data from JSON file "{filename}"'
  )
  return data


def export_json(filename: str, data: list[dict], indent=1, **json_kwargs):
  with open(filename, 'w', encoding='UTF-8') as json_file:
    json.dump(data, json_file, indent=indent, **json_kwargs)
  
  logger.info(
    f'Exported data to JSON file "{filename}"'
  )


def remove_file(filename: str):
  try:
    os.remove(filename)
  except FileNotFoundError:
    logger.warning(
      f'No file to remove "{filename}"'
    )
    raise
  except OSError as e:
    logger.exception(e)
    logger.error(
      f'Could not remove file "{filename}"'
    )
  else:
    logger.info(
      f'Removed file "{filename}"'
    )