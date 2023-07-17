from geoid.bigquery import BigQuery
from geoid.config import Config


def start_generate(args):
  config = Config()
  config.fileio.output_indent = args.indent
  
  querier = BigQuery()
  if args.cities is not None:
    querier.import_list(args.term, args.cities)
  elif args.cities_file is not None:
    querier.import_source(args.term, args.cities_file)
    
  querier.export_json(args.output)