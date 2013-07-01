from selenium import webdriver

from browser import Browser

class Chrome(Browser):
  name = 'chrome'

  def __init__(self):
    Browser.__init__(self)
    self.options = webdriver.ChromeOptions()
    self.options.add_extension('../bin/pixplus.crx')
    self.driver = webdriver.Chrome(chrome_options = self.options)
    pass

  pass