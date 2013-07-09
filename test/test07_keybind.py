import warnings
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from test_base import *

class Test_KeyBind(TestCase):

  # TODO
  #
  # {"key": "popup_caption_scroll_up", "value": "Up"},
  # {"key": "popup_caption_scroll_down", "value": "Down"},
  # {"key": "popup_illust_scroll_up", "value": "Up"},
  # {"key": "popup_illust_scroll_down", "value": "Down"},
  # {"key": "popup_illust_scroll_left", "value": "Left"},
  # {"key": "popup_illust_scroll_right", "value": "Right"},
  # {"key": "popup_illust_scroll_top", "value": "Home"},
  # {"key": "popup_illust_scroll_bottom", "value": "End"},
  # {"key": "popup_illust_page_up", "value": "PageUp"},
  # {"key": "popup_illust_page_down", "value": "PageDown"},

  def prepare(self):
    self.open_test_user()
    self.illust_id_list = self.js('return pixplus.illust.list.map(function(i){return i.id})')
    pass

  def check_id(self, idx):
    self.assertEquals(self.popup_get_illust_data('id'), self.illust_id_list[idx])
    pass

  def check_closed(self):
    self.assertFalse(self.qa('#pp-popup'))
    pass

  def send_keys(self, keys):
    ActionChains(self.driver).send_keys(keys).perform()
    if self.qa('#pp-popup'):
      self.popup_wait_load()
      pass
    pass

  def blur(self):
    self.js('document.activeElement.blur()')
    pass

  def test_move(self):
    self.prepare()

    self.open_popup()
    self.check_id(0)
    self.send_keys('a')
    self.check_closed()

    self.open_popup()
    self.check_id(0)
    self.send_keys(Keys.SPACE)
    self.check_id(1)
    self.send_keys(Keys.ARROW_LEFT)
    self.check_id(0)
    self.send_keys(Keys.ARROW_RIGHT)
    self.check_id(1)
    self.send_keys(Keys.BACK_SPACE)
    self.check_id(0)
    self.send_keys(Keys.END)
    self.check_id(-1)
    self.send_keys(Keys.SPACE)
    self.check_closed()

    self.set_conf('popup.reverse', 1)
    self.open_test_user()

    self.open_popup()
    self.check_id(0)
    self.send_keys(Keys.ARROW_RIGHT)
    self.check_id(1)
    self.send_keys(Keys.ARROW_LEFT)
    self.check_id(0)
    self.send_keys(Keys.ARROW_RIGHT)
    self.check_id(1)
    self.send_keys(Keys.SPACE)
    self.check_id(0)
    self.send_keys('a')
    self.check_id(1)
    self.send_keys(Keys.BACK_SPACE)
    self.check_id(2)
    self.send_keys(Keys.HOME)
    self.check_id(0)
    self.send_keys(Keys.SPACE)
    self.check_closed()
    pass

  def test_close(self):
    self.prepare()

    self.open_popup()
    self.check_id(0)
    self.send_keys('q')
    self.check_closed()

    self.open_popup()
    self.check_id(0)
    self.send_keys(Keys.ESCAPE)
    self.check_closed()
    pass

  def test_header(self):
    self.prepare()

    self.open_popup()
    self.check_id(0)

    title = self.q('#pp-popup-title')
    header = self.q('#pp-popup-header')

    action_chains = ActionChains(self.driver)
    action_chains.move_to_element(title).perform()

    self.assertFalse(self.has_class(header, 'pp-show'))
    self.assertFalse(self.has_class(header, 'pp-hide'))
    self.assertFalse(header.is_displayed())
    self.send_keys('c')
    self.assertTrue(self.has_class(header, 'pp-show'))
    self.assertFalse(self.has_class(header, 'pp-hide'))
    self.assertTrue(header.is_displayed())
    self.send_keys('c')
    self.assertFalse(self.has_class(header, 'pp-show'))
    self.assertFalse(self.has_class(header, 'pp-hide'))
    self.assertFalse(header.is_displayed())

    action_chains.move_to_element(header).perform()

    self.assertFalse(self.has_class(header, 'pp-show'))
    self.assertFalse(self.has_class(header, 'pp-hide'))
    self.assertTrue(header.is_displayed())
    self.send_keys('c')
    self.assertFalse(self.has_class(header, 'pp-show'))
    self.assertTrue(self.has_class(header, 'pp-hide'))
    self.assertFalse(header.is_displayed())
    self.send_keys('c')
    self.assertTrue(self.has_class(header, 'pp-show'))
    self.assertFalse(self.has_class(header, 'pp-hide'))
    self.assertTrue(header.is_displayed())

    action_chains.move_to_element(title).perform()

    self.assertTrue(self.has_class(header, 'pp-show'))
    self.assertFalse(self.has_class(header, 'pp-hide'))
    self.assertTrue(header.is_displayed())
    self.send_keys('c')
    self.assertFalse(self.has_class(header, 'pp-show'))
    self.assertFalse(self.has_class(header, 'pp-hide'))
    self.assertFalse(header.is_displayed())

    action_chains.move_to_element(header).perform()

    self.assertFalse(self.has_class(header, 'pp-show'))
    self.assertFalse(self.has_class(header, 'pp-hide'))
    self.assertTrue(header.is_displayed())


    comment = self.q('#pp-popup-comment')
    self.assertFalse(comment.is_displayed())
    self.send_keys('C')
    self.assertTrue(self.has_class(header, 'pp-show'))
    self.assertTrue(comment.is_displayed())
    self.send_keys('C')
    self.assertTrue(self.has_class(header, 'pp-show'))
    self.assertFalse(comment.is_displayed())
    pass

  def handle_open(self):
    self.js('''
      window.open = function(url) {
        pixplus.test_handle_open = url;
      };
    ''')
    pass

  def poll_open(self, url):
    self.assertTrue(url)
    opened = None
    for i in range(10):
      opened = self.js('''
        return (function() {
          var r = pixplus.test_handle_open;
          pixplus.test_handle_open = null;
          return r;
        })();
      ''')
      if opened:
        break
      time.sleep(1)
      pass

    self.assertEquals(opened, url)
    pass

  def test_open(self):
    self.open('/')
    self.open_popup(1580459)
    self.handle_open()

    self.send_keys('F')
    self.poll_open('/member_illust.php?mode=medium&illust_id=1580459')

    self.send_keys('f')
    self.poll_open('http://i1.pixiv.net/img01/img/pixiv/1580459.jpg')

    self.send_keys('e')
    self.poll_open('/member.php?id=11')

    self.send_keys('r')
    self.poll_open('/member_illust.php?id=11')

    self.send_keys('t')
    self.poll_open('/bookmark.php?id=11')

    self.send_keys('y')
    self.poll_open('/stacc/pixiv')

    self.send_keys('B')
    self.poll_open('/bookmark_detail.php?illust_id=1580459')
    pass

  def test_image_response(self):
    self.open('/')
    self.handle_open()

    self.open_popup(1580459)
    btn = self.q('#pp-popup-button-response:not(.pp-active)')
    self.assertTrue(btn.is_displayed())
    self.send_keys('R')
    self.poll_open('/response.php?illust_id=1580459')

    self.open('/response.php?illust_id=1580459')
    self.handle_open()

    self.open_popup(idx = 2)
    btn = self.q('#pp-popup-button-response.pp-active')
    self.assertTrue(btn.is_displayed())
    self.send_keys('R')
    self.poll_open('/member_illust.php?mode=medium&illust_id=1580459')
    pass

  def test_manga(self):
    self.open('/')
    self.handle_open()

    self.open_popup(6209105)
    self.assertTrue(self.q('#pp-popup-button-manga:not(.pp-active)').is_displayed())

    self.send_keys('f')
    self.poll_open('/member_illust.php?mode=manga&illust_id=6209105')

    self.send_keys('F')
    self.poll_open('/member_illust.php?mode=medium&illust_id=6209105')

    self.send_keys('V')
    self.poll_open('/member_illust.php?mode=manga&illust_id=6209105#pp-manga-thumbnail')

    self.send_keys('v')
    self.assertTrue(self.q('#pp-popup-button-manga.pp-active').is_displayed())

    self.send_keys('f')
    self.poll_open('http://i1.pixiv.net/img01/img/pixiv/6209105_big_p0.jpg')

    self.send_keys('F')
    self.poll_open('/member_illust.php?mode=manga&illust_id=6209105#pp-manga-page-0')

    self.send_keys('V')
    self.poll_open('/member_illust.php?mode=manga&illust_id=6209105#pp-manga-thumbnail')

    self.send_keys('v')
    self.assertTrue(self.q('#pp-popup-button-manga:not(.pp-active)').is_displayed())
    pass

  def test_bookmark(self):
    self.open_test_user()

    self.open_popup()
    bookmark_btn = self.q('#pp-popup-button-bookmark')
    if self.has_class(bookmark_btn, 'pp-active'):
      self.unbookmark()
      self.open_popup()
      bookmark_btn = self.q('#pp-popup-button-bookmark')
      pass

    self.assertFalse(self.has_class(bookmark_btn, 'pp-active'))

    self.send_keys('b')
    self.assertTrue(self.qa('#pp-popup.pp-bookmark-mode'))
    self.assertTrue(self.q('#pp-popup-bookmark-wrapper').is_displayed())

    ####

    input_tag = self.q('#pp-popup-bookmark-wrapper #input_tag')
    tags = self.qa('#pp-popup-bookmark-wrapper .tag-cloud-container .tag')

    input_tag.clear()

    input_tag.send_keys(Keys.ARROW_DOWN)
    self.assertTrue(self.has_class(tags[0], 'pp-tag-select'))

    input_tag.send_keys(Keys.ARROW_RIGHT)
    self.assertFalse(self.has_class(tags[0], 'pp-tag-select'))
    self.assertTrue(self.has_class(tags[1], 'pp-tag-select'))

    input_tag.send_keys(Keys.SPACE)
    self.assertEquals(input_tag.get_attribute('value'), tags[1].get_attribute('data-tag'))
    self.assertTrue(self.has_class(tags[1], 'pp-tag-select'))
    self.assertTrue(self.has_class(tags[1], 'selected'))

    input_tag.send_keys(Keys.SPACE)
    self.assertEquals(input_tag.get_attribute('value'), '')
    self.assertTrue(self.has_class(tags[1], 'pp-tag-select'))
    self.assertFalse(self.has_class(tags[1], 'selected'))

    input_tag.send_keys(Keys.ESCAPE)
    self.assertFalse(self.has_class(tags[1], 'pp-tag-select'))

    ####

    self.blur()

    self.send_keys(Keys.ESCAPE)
    self.assertFalse(self.qa('#pp-popup.pp-bookmark-mode'))
    self.assertFalse(self.q('#pp-popup-bookmark-wrapper').is_displayed())

    self.send_keys('b')
    self.assertTrue(self.qa('#pp-popup.pp-bookmark-mode'))
    self.assertTrue(self.q('#pp-popup-bookmark-wrapper').is_displayed())

    self.blur()

    self.send_keys(Keys.SPACE)
    self.assertFalse(self.qa('#pp-popup.pp-bookmark-mode'))
    self.assertFalse(self.q('#pp-popup-bookmark-wrapper').is_displayed())

    self.popup_reload_and_check_state(lambda: self.has_class(bookmark_btn, 'pp-active'))

    self.unbookmark()
    pass

  def check_has_question(self, popup):
    question = self.qa('#pp-popup-rating .questionnaire')
    if not question:
      return None

    if self.popup_get_illust_data('answered') != False:
      return None

    return question[0]

  def test_question(self):
    self.open_test_user()
    question = self.find_illust(self.check_has_question)
    header = self.q('#pp-popup-header')

    self.send_keys('d')
    self.assertTrue(self.q('.list', question).is_displayed())
    self.assertTrue(self.has_class(header, 'pp-show'))

    self.send_keys('d')
    self.assertFalse(self.q('.list', question).is_displayed())
    self.assertTrue(self.has_class(header, 'pp-show'))

    self.send_keys('d')
    self.assertTrue(self.q('.list', question).is_displayed())
    self.assertTrue(self.has_class(header, 'pp-show'))

    items = self.qa('.list li input[type="button"][data-key]', question)

    for i in range(len(items)):
      self.send_keys(Keys.DOWN)
      self.assertEquals(self.driver.switch_to_active_element(), items[i])
      pass
    self.send_keys(Keys.DOWN)
    self.assertEquals(self.driver.switch_to_active_element(), items[0])

    self.blur()

    for i in range(len(items) - 1, -1, -1):
      self.send_keys(Keys.UP)
      self.assertEquals(self.driver.switch_to_active_element(), items[i])
      pass
    self.send_keys(Keys.UP)
    self.assertEquals(self.driver.switch_to_active_element(), items[-1])

    self.blur()

    if self.repeatable:
      warnings.warn('Skipping answering question')
      return

    answer_idx = int(time.time()) % len(items)
    for i in range(answer_idx + 1):
      self.send_keys(Keys.DOWN)
      pass
    self.assertEquals(self.driver.switch_to_active_element(), items[answer_idx])
    self.assertEquals(items[answer_idx].get_attribute('data-key'), str(answer_idx + 1))
    answer = items[answer_idx].get_attribute('value')

    self.send_keys(Keys.SPACE)

    self.wait_until(lambda d: not self.q('.list', question).is_displayed())

    self.assertFalse(self.q('.list', question).is_displayed())
    self.assertFalse(self.q('.stats', question).is_displayed())
    self.assertIn(answer, self.q('.status', question).text)

    self.blur()

    self.send_keys('d')
    self.assertTrue(self.q('.stats', question).is_displayed())

    self.send_keys('d')
    self.assertFalse(self.q('.stats', question).is_displayed())
    pass

  def test_tag_edit(self):
    self.open_test_user()
    self.set_conf('key.popup_tag_edit_start', 'Shift+t')
    self.open_test_user()

    popup = self.open_popup()
    self.assertFalse(self.has_class(popup, 'pp-tagedit-mode'))
    self.assertFalse(self.q('#pp-popup-tagedit-wrapper').is_displayed())

    self.send_keys('T')
    self.assertTrue(self.has_class(popup, 'pp-tagedit-mode'))
    self.assertTrue(self.q('#pp-popup-tagedit-wrapper').is_displayed())

    self.send_keys(Keys.ESCAPE)
    self.assertFalse(self.has_class(popup, 'pp-tagedit-mode'))
    self.assertFalse(self.q('#pp-popup-tagedit-wrapper').is_displayed())
    pass

  def check_size(self, popup, fit_width, overflow_v, overflow_h):
    data = self.popup_get_illust_data()
    iw, ih = data['size']['width'], data['size']['height']
    sw, sh = self.js('''
      return [document.documentElement.clientWidth,
              document.documentElement.clientHeight];
    ''')

    if (ih > sh) != overflow_v:
      return False
    if (iw > sw) != overflow_h:
      return False

    if ((float(iw) / sw) < (float(ih) / sh)) != fit_width:
      return False

    return True

  def check_scrollbar(self, vertical, horizontal, strict):
    cw, ch, sw, sh, lw, lh = self.js('''
      return (function(s, l) {
        return [s.clientWidth, s.clientHeight, s.scrollWidth, s.scrollHeight,
                l.offsetWidth, l.offsetHeight];
      })(pixplus.popup.dom.image_scroller, pixplus.popup.dom.image_layout);
    ''')

    self.assertEquals(sh > ch, vertical)
    self.assertEquals(sw > cw, horizontal)

    if not vertical:
      self.assertEquals(ch, sh)
      if strict:
        self.assertEquals(ch, lh)
        pass
      pass

    if not horizontal:
      self.assertEquals(cw, sw)
      if strict:
        self.assertEquals(cw, lw)
        pass
      pass
    pass

  def test_resize_mode(self):
    self.open_test_user()
    self.set_conf('popup.big_image', True)
    self.set_conf('popup.fit_short_threshold', 0)

    self.find_illust(self.check_size, True, True, False)
    self.popup_wait_big_image()
    self.check_scrollbar(False, False, False)
    self.send_keys('w')
    time.sleep(2)
    self.check_scrollbar(True, False, False)
    self.send_keys('w')
    time.sleep(2)
    self.check_scrollbar(False, False, False)

    self.find_illust(self.check_size, False, False, True)
    self.popup_wait_big_image()
    self.check_scrollbar(False, False, False)
    self.send_keys('w')
    time.sleep(2)
    self.check_scrollbar(False, True, False)
    self.send_keys('w')
    time.sleep(2)
    self.check_scrollbar(False, False, False)

    self.find_illust(self.check_size, True, True, True)
    self.popup_wait_big_image()
    self.check_scrollbar(False, False, False)
    self.send_keys('w')
    time.sleep(2)
    self.check_scrollbar(True, False, True)
    self.send_keys('w')
    time.sleep(2)
    self.check_scrollbar(True, True, True)
    self.send_keys('w')
    time.sleep(2)
    self.check_scrollbar(False, False, False)

    self.find_illust(self.check_size, False, True, True)
    self.popup_wait_big_image()
    self.check_scrollbar(False, False, False)
    self.send_keys('w')
    time.sleep(2)
    self.check_scrollbar(False, True, True)
    self.send_keys('w')
    time.sleep(2)
    self.check_scrollbar(True, True, True)
    self.send_keys('w')
    time.sleep(2)
    self.check_scrollbar(False, False, False)
    pass

  pass