from geoid.constants import Status

class Metadata:
  def __init__(self):
    self.status    = Status.QUERY_INCOMPLETE
    self.query     = ''
    self.lang      = ''
    self.timestamp = 0