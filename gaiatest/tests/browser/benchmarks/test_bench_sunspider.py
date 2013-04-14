# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import time
from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser


class TestBenchSunspider(GaiaTestCase):

    _start_page = 'http://people.mozilla.com/~npierron/sunspider/hosted/'
    _start_now_locator = ('css selector', 'body > p > a')

    _console_locator = ('id', 'console')

    def setUp(self):
        GaiaTestCase.setUp(self)

        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

    def test_sunspider(self):
        # Bug 860516
        browser = Browser(self.marionette)
        browser.launch()

        browser.go_to_url(self._start_page)
        browser.switch_to_content()
        self.verify_home_page()
        start_now_link = self.marionette.find_element(*self._start_now_locator)

        # wait 30s, to let the system settle.
        time.sleep(15)

        # scroll to the link location & start the benchmark
        start_now_link.single_tap()
        self.marionette.tap(start_now_link)

        # Switch to the chrome, because the page will be automatically
        # redirected as soon as the benchmark is complete
        browser.switch_to_chrome()

        # wait 4 minutes, to let the becnhmark complete.
        time.sleep(4 * 60)
        browser.switch_to_content()
        self.verify_finished()

        self.print_results()

    def verify_home_page(self):
        self.wait_for_element_present(*self._start_now_locator)
        link = self.marionette.find_element(*self._start_now_locator)
        self.assertTrue(link.text == 'Start Now!', 'The sunspider page is not rendered.')

    def verify_finished(self):
        self.wait_for_element_displayed(*self._console_locator)

    def print_results(self):
        # Return a list of lines, as the full string is too large for
        # marionette.
        result = self.marionette.execute_script("""
          return document.getElementById('console').innerHTML.split('<br>');
        """)

        print "\n\nShell-like sunspider results:"
        print "\n".join(result)
        print "End of shell-like results."
