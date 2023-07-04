from geoid.constants import status

class Metadata:
  def __init__(
    self,
    query:str='',
    lang:str='',
    timestamp:int=0
  ):
    self.status    = status.QUERY_INCOMPLETE
    self.query     = query
    self.lang      = lang
    self.timestamp = timestamp