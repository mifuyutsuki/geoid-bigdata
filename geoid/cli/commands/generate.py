from geoid.config import Config
from geoid.common import io


def start_generate(args):
  config = Config()
  config.fileio.output_indent = args.indent

  data = []
  if args.sourcelist is not None:
    data = io.generate_data(args.term, args.sourcelist)
  elif args.sourcefile is not None:
    data = io.generate_data_from_txt(args.term, args.sourcefile)

  io.export_json(args.outputfile, data, indent=args.indent)