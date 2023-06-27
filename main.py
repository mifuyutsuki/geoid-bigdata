import argparse
from geoid import begin, __version__
from geoid.config import Config

parser = argparse.ArgumentParser(
  description=
    'GMaps places data mining program for Big Data use, '
    'designed for Indonesia locations.\n'
    'Example usage: keyword "pariwisata" '
    '--> search "pariwisata <cityname>" for all <cityname> in <cities>.\n'
    '\n'
    'Query "<keyword> <cityname>" in batch mode with -i <filename>.\n'
    'Query "<keyword>" in single mode without using -i.',
  formatter_class=argparse.RawDescriptionHelpFormatter
)

parser.add_argument(
  'keyword', type=str,
  help='Search keyword'
)
parser.add_argument(
  'output', type=str,
  help='Output filename (JSON)'
)

parser.add_argument(
  '--version',
  action='version',
  version=f'geoid-BigData {__version__}'
)

parser.add_argument(
  '-i', type=str,
  help='Source cities filename for batch mode.',
  nargs='?',
  action='store',
  default=None,
  metavar='<filename>',
  dest='cities'
)

parser.add_argument(
  '-depth', type=int,
  help='Search depth; set 0 for endless. Default: 0',
  action='store',
  default=0,
  metavar='<number>',
  dest='depth'
)
parser.add_argument(
  '-indent', type=int,
  help='Set output file indent by number of spaces. Default: 2',
  action='store',
  default=2,
  metavar='<number>',
  dest='indent'
)
parser.add_argument(
  '-browser', type=str,
  choices=['firefox', 'chrome'],
  help='Use a particular supported browser client. Default: firefox',
  action='store',
  default='firefox',
  dest='browser'
)
parser.add_argument(
  '--show',
  help='Display browser client.',
  action='store_true',
  dest='show'
)
parser.add_argument(
  '--timestamp',
  help='Include timestamp in output filename with {timestamp} in <output>.',
  action='store_true',
  dest='timestamp'
)
parser.add_argument(
  '--keep-autosave',
  help='Don\'t remove the generated autosave on completion. Autosaves are not postprocessed.',
  action='store_true',
  dest='keep_autosave'
)
parser.add_argument(
  '--no-filter',
  help='Post: (Batch mode only) Don\'t filter results with mismatched cities.',
  action='store_false',
  dest='filter'
)
parser.add_argument(
  '--flat',
  help='Post: Flatten query results to only a one-layer array of objects.',
  action='store_true',
  dest='flatten'
)
parser.add_argument(
  '--ascii',
  help='Post: Convert text in field strings to ASCII.',
  action='store_true',
  dest='convert_ascii'
)
parser.add_argument(
  '--replace-newline',
  help='Post: Replace newlines in field strings with semicolons.',
  action='store_true',
  dest='replace_newline'
)

def main():
  args = parser.parse_args()

  if args.timestamp:
    if "{timestamp}" not in args.output:
      print(
        'Specify timestamp location in the output filename using {timestamp} '
        'to use the timestamp option'
      )
      quit()
  
  config = Config()
  config.bigquerier.query_depth    = args.depth
  config.fileio.output_indent      = args.indent
  config.webclient.webclient       = args.browser
  config.webclient.show            = args.show
  config.fileio.use_timestamp_name = args.timestamp
  config.fileio.keep_autosave      = args.keep_autosave
  config.postproc.filter           = args.filter
  config.postproc.flatten          = args.flatten
  config.postproc.convert_ascii    = args.convert_ascii
  config.postproc.replace_newline  = args.replace_newline

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
    begin(
      keyword=args.keyword,
      source_file=args.cities,
      output_file=args.output,
      use_config=config
    )

if __name__ == '__main__':
  main()