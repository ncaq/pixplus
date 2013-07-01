import os
import subprocess
import time
import httplib

from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common import utils as selutils

from browser import Browser
import util

class BrowserSeleniumServer(Browser):
  selenium_server_url = 'https://selenium.googlecode.com/files/selenium-server-standalone-2.33.0.jar'

  def __init__(self):
    Browser.__init__(self)
    self.start_server()
    pass

  def create_driver(self, desired_capabilities):
    self.driver = RemoteWebDriver(
      'http://localhost:%d/wd/hub' % self.server_port,
      desired_capabilities = desired_capabilities
      )
    pass

  def download_selenium_server(self):
    filename = self.selenium_server_url.split('/').pop()
    if not os.path.exists(filename):
      util.download(self.selenium_server_url, filename)
      pass
    return filename

  def start_server(self):
    jar = self.download_selenium_server()
    self.server_port = selutils.free_port()

    self.server_log_fp = open('selenium-%d.log' % time.time(), 'w')
    self.server_process = subprocess.Popen(
      ['java', '-jar', jar, '-port', str(self.server_port)],
      stdout = self.server_log_fp, stderr = subprocess.STDOUT
      )

    while not selutils.is_connectable(self.server_port):
      time.sleep(1)
      pass
    pass

  def quit(self):
    try:
      Browser.quit(self)
    except httplib.BadStatusLine:
      pass

    self.server_process.kill()
    self.server_process.wait()
    self.server_log_fp.close()
    pass

  pass