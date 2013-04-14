# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import time
from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser


class TestBenchKraken(GaiaTestCase):

    _start_page = 'http://people.mozilla.com/~npierron/kraken/hosted/index.html'
    _run_locator = ('css selector', '#results > p > a')

    _console_locator = ('id', 'console')

    def setUp(self):
        GaiaTestCase.setUp(self)

        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

    def test_kraken(self):
        # Bug 860516
        browser = Browser(self.marionette)
        browser.launch()

        browser.go_to_url(self._start_page)
        browser.switch_to_content()
        self.verify_home_page()

        run_link = self.marionette.find_element(*self._run_locator)

        # wait 30s, to let the system settle.
        time.sleep(30)

        # start the benchmark
        self.marionette.tap(run_link)

        # Switch to the chrome, because the page will be automatically
        # redirected as soon as the benchmark is complete
        browser.switch_to_chrome()

        # wait 8 minutes, to let the becnhmark complete.
        time.sleep(8 * 60)
        browser.switch_to_content()
        self.verify_finished()

        self.print_results()

    def verify_home_page(self):
        self.wait_for_element_present(*self._run_locator)
        link = self.marionette.find_element(*self._run_locator)
        self.assertTrue(link.text == 'Begin', 'The kraken page is not rendered.')

    def verify_finished(self):
        self.wait_for_element_present(*self._run_locator)
        link = self.marionette.find_element(*self._run_locator)
        self.assertTrue(link.text == 'Run Again', 'The kraken page is not rendered.')

    def print_results(self):
        result = self.marionette.execute_script("""
          return document.getElementById('console').innerHTML
                   .replace(/<.?a[^>]*>/g, '').split('<br>')
        """)

        print "\n\nShell-like kraken results:"
        print "\n".join(result)
        print "End of shell-like results."
