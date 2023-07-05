from geoid.constants import Status

class Metadata:
  def __init__(
    self,
    query:str='',
    lang:str='',
    timestamp:int=0
  ):
    self.status    = Status.QUERY_INCOMPLETE
    self.query     = query
    self.lang      = lang
    self.timestamp = timestamp