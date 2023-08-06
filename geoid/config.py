# Copyright (c) 2023 Mifuyu (mifuyutsuki@proton.me)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# TODO: Load configuration from a config.toml


class QueryConfig:
  def __init__(self):
    self.initial_pause_seconds   = 0.0
    self.loading_timeout_seconds = 15.0
    self.scroll_wait_seconds     = 2.5
    self.scroll_retries          = 5
    self.depth                   = 3
    self.lang                    = 'id'

class PostprocConfig:
  def __init__(self):
    self.filter          = False
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
    self.webclient          = 'chrome'
    self.show               = False

class Config:
  def __init__(self):
    self.query      = QueryConfig()
    self.postproc   = PostprocConfig()
    self.fileio     = FileIOConfig()
    self.webclient  = WebClientConfig()