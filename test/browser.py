import os
import shutil
import time
import json
import base64

from PIL import Image

try:
  import http.client as http_client
except ImportError:
  import httplib as http_client
  pass

from selenium.webdriver import ActionChains
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert

import util

class Browser:
  name = None
  capname = None
  supports_alert = True

  def __init__(self):
    self.driver = None
    self.profiledir = None
    pass

  def start(self):
    caps = {}
    caps.update(getattr(DesiredCapabilities, self.capname))
    self.prepare_caps(caps)
    self.driver = WebDriver(
      'http://localhost:%d/wd/hub' % self.args.server_port,
      desired_capabilities = caps
      )
    self.driver.implicitly_wait(2)
    pass

  def quit(self):
    try:
      self.driver.quit()
    except http_client.BadStatusLine:
      pass
    pass

  def create_profile(self):
    self.profiledir = os.path.join(self.testdir, 'profile', self.name)
    if os.path.exists(self.profiledir):
      shutil.rmtree(self.profiledir)
      pass
    os.makedirs(self.profiledir)
    return self.profiledir

  def set_window_size(self, width, height):
    self.driver.set_window_size(width, height)
    pass

  @property
  def url(self):
    return self.driver.current_url

  def wait_page_load(self):
    time.sleep(1)
    self.wait_until(lambda d: self.js('return document&&document.readyState==="complete"'))
    pass

  def open(self, url):
    self.driver.get(url)
    self.wait_page_load()
    pass

  def reload(self):
    self.open(self.url)
    pass

  def wait_until(self, callback):
    wait = WebDriverWait(self.driver, 20)
    return wait.until(callback)

  def ac(self):
    return ActionChains(self.driver)

  def q(self, selector, context = None):
    if context is None:
      return self.driver.find_element_by_css_selector(selector)
    return context.find_element_by_css_selector(selector)

  def qa(self, selector, context = None):
    if context is None:
      return self.driver.find_elements_by_css_selector(selector)
    return context.find_elements_by_css_selector(selector)

  def x(self, xpath):
    return self.driver.find_element_by_xpath(xpath)

  def xa(self, xpath):
    return self.driver.find_elements_by_xpath(xpath)

  def alert_accept(self):
    if self.supports_alert:
      Alert(self.driver).accept()
    else:
      raise RuntimeError('%s not supports alert handling' % self.name)
    pass

  def js(self, script, *args):
    return self.driver.execute_script(script, *args)

  def geom(self, element):
    return tuple(map(round, self.js('''
      var elem = arguments[0];
      var rect = elem.getBoundingClientRect();
      return [rect.left, rect.top, rect.width, rect.height];
    ''', element)))

  def screen_size(self):
    sw, sh = self.js('''
      return [document.documentElement.clientWidth,
              document.documentElement.clientHeight];
    ''')
    return sw, sh


  def set_cookie(self, name, value, domain, path):
    expires = ''
    if value is None:
      value = ''
      expires = '; expires=Thu, 01 Jan 1970 00:00:00 GMT'
      pass
    cookie = '%s=%s; domain=%s; path=%s%s' % (name, value, domain, path, expires)
    self.js('document.cookie=%s' % json.dumps(cookie))
    pass

  def screenshot(self):
    ss = self.driver.get_screenshot_as_base64().encode('ascii')
    io = util.BytesIO(base64.b64decode(ss))
    return Image.open(io).convert('RGB')

  pass
