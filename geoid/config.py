class QueryConfig:
  def __init__(self):
    self.loading_timeout_seconds = 15.0
    self.scroll_wait_seconds     = 2.5
    self.scroll_retries          = 5
    self.depth                   = 3
    self.lang                    = 'id'

class PostprocConfig:
  def __init__(self):
    self.filter          = True
    self.flatten         = False
    self.convert_ascii   = False
    self.replace_newline = False

class FileIOConfig:
  def __init__(self):
    self.autosave_filename  = '.autosave'
    self.autosave_every     = 1
    self.keep_autosave      = False
    self.output_indent      = 2
    self.use_timestamp_name = False
  
class WebClientConfig:
  def __init__(self) -> None:
    self.webclient          = 'firefox'
    self.show               = False

class Config:
  def __init__(self):
    self.query      = QueryConfig()
    self.postproc   = PostprocConfig()
    self.fileio     = FileIOConfig()
    self.webclient  = WebClientConfig()