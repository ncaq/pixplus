import time

from selenium.webdriver import ActionChains

from test_base import TestCase

class Test_Rate(TestCase):

  def test_rate(self):
    self.open_test_user()
    if self.browser.name == 'opera':
      self.driver.execute_script('pixplus.conf.general.rate_confirm=false')
      pass

    rating = self.find_illust(lambda popup: self.qa('#pp-popup-rating .score .rating:not(.rated)', popup))
    rating = rating[0]
    self.driver.execute_script('pixplus.popup.show_caption()')

    action_chains = ActionChains(self.driver)
    action_chains.move_to_element_with_offset(rating, 220, 10).perform()
    time.sleep(1)
    action_chains.click().perform()

    self.alert_accept()

    rate = self.q('.rate', rating)
    self.assertEqual(rate.size['width'], 234)

    self.assertTrue(self.qa('#pp-popup-rating .score .rating.rated'))
    self.popup_reload()
    self.assertTrue(self.qa('#pp-popup-rating .score .rating.rated'))
    pass

  pass