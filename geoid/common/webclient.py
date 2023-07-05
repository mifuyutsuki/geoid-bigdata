from selenium import webdriver


def init_firefox(*, show_client=False, use_options=None):
  options = use_options if use_options else webdriver.FirefoxOptions()
  if not show_client:
    options.add_argument('-headless')
  driver = webdriver.Firefox(options=options)

  return driver


def init_chrome(*, show_client=False, use_options=None):
  options = use_options if use_options else webdriver.ChromeOptions()
  if not show_client:
    options.add_argument('--headless=new')
  driver = webdriver.Chrome(options=options)

  return driver