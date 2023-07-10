from geoid import __version__
from geoid.config import Config

from .run import run_batch
from .parser import build

def start():
  parser = build()
  args = parser.parse_args()

  if args.timestamp:
    if "{timestamp}" not in args.output:
      print(
        'Specify timestamp location in the output filename using {timestamp} '
        'to use the timestamp option'
      )
      quit()
  
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
    #   f'Starting in single mode. Query: "{args.keyword}"'
    # )
    print(
      'Single mode is still work in progress.'
    )
  else:
    print(
      f'Starting in batch mode. Query: "{args.keyword} <cityname>"'
    )
    run_batch(
      keyword=args.keyword,
      source_file=args.cities,
      output_file=args.output,
      use_config=config
    )