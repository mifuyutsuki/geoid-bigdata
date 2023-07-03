class Metadata:
  STATUS_INCOMPLETE = 0
  STATUS_COMPLETE   = 1
  STATUS_ERRORED    = 2

  def __init__(
    self,
    query:str='',
    lang:str='',
    timestamp:int=STATUS_INCOMPLETE
  ):
    self.status    = self.STATUS_INCOMPLETE
    self.query     = query
    self.lang      = lang
    self.timestamp = timestamp