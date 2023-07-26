# Copyright (c) 2023 mifuyutsuki

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

from selenium import webdriver
from selenium_stealth import stealth


def init_firefox(*, show_client=False, use_options=None):
  options = use_options if use_options else webdriver.FirefoxOptions()
  if not show_client:
    options.add_argument('-headless')
  driver = webdriver.Firefox(options=options)

  return driver


def init_chrome(*, show_client=False, use_options=None):
  options = use_options if use_options else webdriver.ChromeOptions()
  options.add_experimental_option('excludeSwitches', ['enable-automation'])
  options.add_experimental_option('useAutomationExtension', False)
  if not show_client:
    options.add_argument('--headless=new')
    
  driver = webdriver.Chrome(options=options)

  #: Will raise an exception, but this is fine
  #: Prior steps of stealth() are functional
  try:
    stealth(driver, fix_hairline=True)
  except Exception:
    pass

  return driver