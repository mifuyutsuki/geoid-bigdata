class Metadata:
  def __init__(
    self,
    query: str,
    lang: str,
    timestamp: int
  ):
    self._query     = query
    self._lang      = lang
    self._timestamp = timestamp
  
  @property
  def query(self):
    return self._query
  
  @property
  def lang(self):
    return self._lang
  
  @property
  def timestamp(self):
    return self._timestamp