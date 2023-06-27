class BigQuerierConfig:
  def __init__(self):
    self.loading_timeout_seconds = 15.0
    self.scroll_wait_seconds     = 2.5
    self.scroll_retries          = 5
    self.autosave_every          = 1
    self.keep_autosave           = False
    self.query_depth             = 0
    self.query_lang              = 'id'

class PostprocConfig:
  def __init__(self):
    self.filter          = True
    self.flatten         = False
    self.convert_ascii   = False
    self.replace_newline = False

class Config:
  def __init__(self):
    self.bigquerier = BigQuerierConfig()
    self.postproc   = PostprocConfig()