from geoid.version import __version__
import argparse


def build():
  """
  Create an argument parser for GeoID CLI.

  Returns:
      ArgumentParser object to be used for parsing system arguments.
  """

  parser = argparse.ArgumentParser(
    description=
      'Maps data scraper-parser for Indonesia places.',
    usage='%(prog)s [-h] [--version] term (-f filename | -l location [location ...]) [options]',
    prog='geoid',
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter
  )

  help_args = parser.add_argument_group('Help')
  help_args.add_argument(
    '-h', '--help',
    action='help',
    help='Show this help message and exit'
  )
  help_args.add_argument(
    '--version',
    action='version',
    version=f'geoid-bigdata {__version__}',
    help='Show program\'s version number and exit'
  )

  required_args = parser.add_argument_group('Required')
  required_args.add_argument(
    'term', type=str,
    help='Search term'
  )
  input_group = required_args.add_mutually_exclusive_group(required=True)
  input_group.add_argument(
    '-f', type=str,
    help='JSON filename containing cities data',
    nargs='?',
    action='store',
    metavar='filename',
    dest='cities_file'
  )
  input_group.add_argument(
    '-l', type=str,
    help='City or cities to query by name',
    nargs='*',
    action='store',
    metavar='location',
    dest='cities'
  )
  required_args.add_argument(
    '-o', type=str,
    required=True,
    help='Filename of output JSON containing search results',
    nargs='?',
    action='store',
    metavar='filename',
    dest='output'
  )

  options_args = parser.add_argument_group('Options')
  options_args.add_argument(
    '-depth', type=int,
    help='Search depth; set 0 for endless (default: 1)',
    action='store',
    default=1,
    metavar='<number>',
    dest='depth'
  )
  options_args.add_argument(
    '-indent', type=int,
    help='Set output file indent by number of spaces (default: 2)',
    action='store',
    default=2,
    metavar='<number>',
    dest='indent'
  )
  options_args.add_argument(
    '-browser', type=str,
    choices=['firefox', 'chrome'],
    help='Use a particular supported browser client (default: firefox)',
    action='store',
    default='firefox',
    dest='browser'
  )
  options_args.add_argument(
    '-init-pause', type=float,
    help='Pause for a set number of seconds after access (default: 0.0)',
    action='store',
    default=0.0,
    dest='init_pause'
  )
  options_args.add_argument(
    '--show',
    help='Display browser client',
    action='store_true',
    dest='show'
  )
  options_args.add_argument(
    '--timestamp',
    help='Include timestamp in output filename with {timestamp} in filename',
    action='store_true',
    dest='timestamp'
  )
  options_args.add_argument(
    '--keep-autosave',
    help='Don\'t remove the generated autosave on completion; autosaves are not postprocessed',
    action='store_true',
    dest='keep_autosave'
  )
  options_args.add_argument(
    '--filter',
    help='Filter query results with mismatched cities',
    action='store_true',
    dest='filter'
  )
  options_args.add_argument(
    '--flat',
    help='Flatten query results to only a one-layer array of objects',
    action='store_true',
    dest='flatten'
  )
  options_args.add_argument(
    '--ascii',
    help='Convert text in query results values to ASCII',
    action='store_true',
    dest='convert_ascii'
  )
  options_args.add_argument(
    '--replace-newline',
    help='Replace newlines in query results values with semicolons',
    action='store_true',
    dest='replace_newline'
  )

  return parser