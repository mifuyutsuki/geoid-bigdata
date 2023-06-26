import argparse
from geoid import begin

parser = argparse.ArgumentParser(
  prog='geoid',
  description=
    'Selenium-based GMaps data mining program for Big Data use, '
    'specifically designed for Indonesia locations. '
    'Example usage: keyword "pariwisata" '
    '--> search "pariwisata <cityname>" for all cityname in <source>.',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument(
  'keyword', type=str,
  help='Search keyword'
)
parser.add_argument(
  'source', type=str,
  help='Source containing cities data (JSON)'
)
parser.add_argument(
  'output', type=str,
  help='Output file (JSON)'
)

parser.add_argument(
  '-d', '--depth', type=int,
  help='Search depth; set 0 for endless',
  action='store',
  default=0,
  metavar='number',
  dest='depth'
)
parser.add_argument(
  '-i', '--indent', type=int,
  help='Set output file indent by number of spaces',
  action='store',
  default=2,
  metavar='number',
  dest='indent'
)
parser.add_argument(
  '-b', '--browser', type=str,
  choices=['firefox', 'chrome'],
  help='Use a particular browser client',
  action='store',
  default='firefox',
  dest='browser'
)
parser.add_argument(
  '-s', '--show',
  help='Display browser client',
  action='store_true',
  dest='show'
)
parser.add_argument(
  '-t', '--timestamp',
  help='Include timestamp in output filename with {timestamp}',
  action='store_true',
  dest='timestamp'
)

if __name__ == '__main__':
  args = parser.parse_args()

  if args.timestamp:
    if "{timestamp}" not in args.output:
      print(
        'Specify timestamp location in the output filename using {timestamp} '
        'to use the timestamp option'
      )
      quit()

  begin(
    keyword=args.keyword,
    source_file=args.source,
    output_file=args.output,
    query_depth=args.depth,
    indent=args.indent,
    web_client=args.browser,
    show_client=args.show,
    use_timestamp=args.timestamp
  )