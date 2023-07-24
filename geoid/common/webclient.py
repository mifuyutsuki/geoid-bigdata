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