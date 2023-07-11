from geoid.version import __version__
from geoid.config import Config

from .run import run_batch
from .parser import build

import time


def start():
  """
  Launch GeoID using the provided system arguments.

  Called when launching GeoID from the command line with `python -m geoid`.
  """

  parser = build()
  args = parser.parse_args()

  if args.timestamp:
    if "{timestamp}" not in args.output:
      print(
        'Specify timestamp location in the output filename using {timestamp} '
        'to use the timestamp option'
      )
      return
    else:      
      timestamp = time.strftime('%Y%m%d_%H%M%S')
      output_file = args.output.replace("{timestamp}", timestamp)
  else:
    output_file = args.output
  
  config = Config()
  config.query.depth                 = args.depth
  config.fileio.output_indent        = args.indent
  config.webclient.webclient         = args.browser
  config.query.initial_pause_seconds = args.init_pause
  config.webclient.show              = args.show
  config.fileio.use_timestamp_name   = args.timestamp
  config.fileio.keep_autosave        = args.keep_autosave
  config.postproc.filter             = args.filter
  config.postproc.flatten            = args.flatten
  config.postproc.convert_ascii      = args.convert_ascii
  config.postproc.replace_newline    = args.replace_newline

  if args.cities is None:
    # print(
    #   f'Starting single query.'
    #   f'Query keyword: "{args.keyword}"'
    # )
    print(
      'Single mode is still work in progress.'
    )
  else:
    print(
      f'Starting batch query.\n'
      f'Query keyword: "{args.keyword} <cityname>"'
    )
    run_batch(
      keyword=args.keyword,
      source_file=args.cities,
      output_file=output_file,
      use_config=config
    )