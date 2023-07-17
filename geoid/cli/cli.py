from geoid.version import __version__
from . import commands

import argparse


def start():
  """
  Launch GeoID using the provided system arguments.

  Called when launching GeoID from the command line with `python -m geoid`.
  """

  parser = build()
  args = parser.parse_args()
  args.func(args)


def build():
  """
  Create an argument parser for GeoID CLI.

  Returns:
      ArgumentParser object to be used for parsing system arguments.
  """

  # ===========================================================================

  parser = argparse.ArgumentParser(
    description=
      'Maps data scraper-parser for Indonesia places.',
    prog='geoid',
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter
  )
  subparsers = parser.add_subparsers(
    title='subcommands',
    description='valid subcommands',
    help='additional help',
    required=True
  )

  # ===========================================================================

  help_args = parser.add_argument_group('help')
  help_args.add_argument(
    '-h', '--help',
    action='help',
    help='show this help message and exit'
  )
  help_args.add_argument(
    '--version',
    action='version',
    version=f'geoid-bigdata {__version__}',
    help='show program\'s version number and exit'
  )

  # ===========================================================================

  global_args = parser.add_argument_group('global options')
  global_args.add_argument(
    '--show-info-logs',
    action='store_true',
    help='show INFO logs to terminal in addition to WARNING logs',
    dest='show_info'
  )

  # ===========================================================================

  parser_query = subparsers.add_parser(
    'query',
    help='launch a query',
    usage='%(prog)s term (-f filename | -l location [location ...]) -o filename [options]'
  )
  parser_query.set_defaults(func=commands.start_query)

  # ---------------------------------------------------------------------------

  query_required_args = parser_query.add_argument_group('required')
  query_required_args.add_argument(
    'term', type=str,
    help='search term'
  )
  query_input_group = query_required_args.add_mutually_exclusive_group(required=True)
  query_input_group.add_argument(
    '-f', type=str,
    help='JSON filename containing cities data',
    nargs='?',
    action='store',
    metavar='filename',
    dest='cities_file'
  )
  query_input_group.add_argument(
    '-l', type=str,
    help='city or cities to query by name',
    nargs='*',
    action='store',
    metavar='location',
    dest='cities'
  )
  query_required_args.add_argument(
    '-o', type=str,
    required=True,
    help='filename of output JSON containing search results',
    nargs='?',
    action='store',
    metavar='filename',
    dest='output'
  )

  # ---------------------------------------------------------------------------

  query_options_args = parser_query.add_argument_group('command options')
  query_options_args.add_argument(
    '-depth', type=int,
    help='search depth; set 0 for endless (default: 1)',
    action='store',
    default=1,
    metavar='<number>',
    dest='depth'
  )
  query_options_args.add_argument(
    '-indent', type=int,
    help='set output file indent by number of spaces (default: 2)',
    action='store',
    default=2,
    metavar='<number>',
    dest='indent'
  )
  query_options_args.add_argument(
    '-browser', type=str,
    choices=['firefox', 'chrome'],
    help='use a particular supported browser client (default: firefox)',
    action='store',
    default='firefox',
    dest='browser'
  )
  query_options_args.add_argument(
    '-init-pause', type=float,
    help='pause for a set number of seconds after access (default: 0.0)',
    action='store',
    default=0.0,
    dest='init_pause'
  )
  query_options_args.add_argument(
    '--show',
    help='display browser client',
    action='store_true',
    dest='show'
  )
  query_options_args.add_argument(
    '--timestamp',
    help='include timestamp in output filename with {timestamp} in filename',
    action='store_true',
    dest='timestamp'
  )
  query_options_args.add_argument(
    '--keep-autosave',
    help='don\'t remove the generated autosave on completion; autosaves are not postprocessed',
    action='store_true',
    dest='keep_autosave'
  )
  query_options_args.add_argument(
    '--filter',
    help='filter query results with mismatched cities',
    action='store_true',
    dest='filter'
  )
  query_options_args.add_argument(
    '--flat',
    help='flatten query results to only a one-layer array of objects',
    action='store_true',
    dest='flatten'
  )
  query_options_args.add_argument(
    '--ascii',
    help='convert text in query results values to ASCII',
    action='store_true',
    dest='convert_ascii'
  )
  query_options_args.add_argument(
    '--replace-newline',
    help='replace newlines in query results values with semicolons',
    action='store_true',
    dest='replace_newline'
  )

  # ===========================================================================

  parser_query = subparsers.add_parser(
    'generate',
    help='generate a starter queries data for editing and later use',
    usage='%(prog)s term (-f filename | -l location [location ...]) -o filename [options]'
  )
  parser_query.set_defaults(func=commands.start_generate)

  # ---------------------------------------------------------------------------

  generate_required_args = parser_query.add_argument_group('Required')
  generate_required_args.add_argument(
    'term', type=str,
    help='search term'
  )
  generate_input_group = generate_required_args.add_mutually_exclusive_group(required=True)
  generate_input_group.add_argument(
    '-f', type=str,
    help='JSON filename containing cities data',
    nargs='?',
    action='store',
    metavar='filename',
    dest='cities_file'
  )
  generate_input_group.add_argument(
    '-l', type=str,
    help='city or cities to query by name',
    nargs='*',
    action='store',
    metavar='location',
    dest='cities'
  )
  generate_required_args.add_argument(
    '-o', type=str,
    required=True,
    help='filename of output JSON containing search results',
    nargs='?',
    action='store',
    metavar='filename',
    dest='output'
  )

  # ---------------------------------------------------------------------------

  generate_options_args = parser_query.add_argument_group('Options')
  generate_options_args.add_argument(
    '-indent', type=int,
    help='set output file indent by number of spaces (default: 2)',
    action='store',
    default=2,
    metavar='<number>',
    dest='indent'
  )

  return parser