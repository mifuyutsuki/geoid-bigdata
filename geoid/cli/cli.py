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
    '-v', '--version',
    action='version',
    version=f'geoid-bigdata {__version__}',
    help='show program\'s version number and exit'
  )

  # ===========================================================================

  # global_args = parser.add_argument_group('global options')
  # global_args.add_argument(
  #   '--show-info-logs',
  #   action='store_true',
  #   help='show INFO logs to terminal in addition to WARNING logs',
  #   dest='show_info'
  # )

  # ===========================================================================

  parser_query = subparsers.add_parser(
    'query',
    help='launch a query',
    description=
      'Launch a query using a queries data file. Each query in a queries data '
      'file contains information on the location keyword and the query '
      'keyword. To generate a queries data file, see help for geoid generate.',
    usage='%(prog)s sourcefile -o outputfile [options]',
  )
  parser_query.set_defaults(func=commands.start_query)

  # ---------------------------------------------------------------------------

  query_required_args = parser_query.add_argument_group('required')
  query_required_args.add_argument(
    'sourcefile', type=str,
    help='input queries data JSON file'
  )
  query_required_args.add_argument(
    '-o', '--output', type=str,
    required=True,
    help='output queries data JSON file with search results',
    nargs='?',
    action='store',
    metavar='outputfile',
    dest='outputfile'
  )

  # ---------------------------------------------------------------------------

  query_options_args = parser_query.add_argument_group('command options')
  query_options_args.add_argument(
    '-d', '--depth', type=int,
    help='search depth; set 0 for endless (default: 1)',
    action='store',
    default=1,
    metavar='<number>',
    dest='depth'
  )
  query_options_args.add_argument(
    '-b', '--browser', type=str,
    choices=['chrome', 'firefox'],
    help='use a particular supported browser client (default: chrome)',
    action='store',
    default='chrome',
    dest='browser'
  )
  query_options_args.add_argument(
    '-s', '--show',
    help='display browser client',
    action='store_true',
    dest='show'
  )
  query_options_args.add_argument(
    '-t', '--timestamp',
    help='include timestamp in output filename with {timestamp} in filename',
    action='store_true',
    dest='timestamp'
  )
  query_options_args.add_argument(
    '-A', '--keep-autosave',
    help='don\'t remove the generated autosave on completion; autosaves are not postprocessed',
    action='store_true',
    dest='keep_autosave'
  )
  query_options_args.add_argument(
    '-in', '--indent', type=int,
    help='set output file indent by number of spaces (default: 2)',
    action='store',
    default=2,
    metavar='<number>',
    dest='indent'
  )
  query_options_args.add_argument(
    '-ip', '--init-pause', type=float,
    help='pause for a set number of seconds after access (default: 0.0)',
    action='store',
    default=0.0,
    metavar='<float>',
    dest='init_pause'
  )
  query_options_args.add_argument(
    '-fi', '--filter',
    help='filter query results with mismatched cities',
    action='store_true',
    dest='filter'
  )
  query_options_args.add_argument(
    '-fl', '--flat',
    help='flatten query results to only a one-layer array of objects',
    action='store_true',
    dest='flatten'
  )
  query_options_args.add_argument(
    '-as', '--ascii',
    help='convert text in query results values to ASCII',
    action='store_true',
    dest='convert_ascii'
  )
  query_options_args.add_argument(
    '-rn', '--replace-newline',
    help='replace newlines in query results values with semicolons',
    action='store_true',
    dest='replace_newline'
  )

  # ===========================================================================

  parser_query = subparsers.add_parser(
    'generate',
    help='generate a starter queries data for editing and later use',
    description=
      'Generate a queries data file. The command accepts a list of cities '
      'either in the argument or in a specified text file. Each non-blank line '
      'in the text file is a city.',
    usage=
      '%(prog)s term (-f filename | -l location [location ...]) '
      '-o filename [options]'
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
    '-f', '--file', type=str,
    help='text file containing list of cities',
    nargs='?',
    action='store',
    metavar='filename',
    dest='sourcefile'
  )
  generate_input_group.add_argument(
    '-l', '--list', type=str,
    help='list of city or cities to query by name',
    nargs='*',
    action='store',
    metavar='location',
    dest='sourcelist'
  )
  generate_required_args.add_argument(
    '-o', '--output', type=str,
    required=True,
    help='output queries data JSON',
    nargs='?',
    action='store',
    metavar='filename',
    dest='outputfile'
  )

  # ---------------------------------------------------------------------------

  generate_options_args = parser_query.add_argument_group('Options')
  generate_options_args.add_argument(
    '-in', '--indent', type=int,
    help='set output file indent by number of spaces (default: 2)',
    action='store',
    default=2,
    metavar='<number>',
    dest='indent'
  )

  return parser