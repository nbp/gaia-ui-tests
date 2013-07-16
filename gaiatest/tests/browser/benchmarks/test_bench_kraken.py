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
        self.connect_to_local_area_network()

    def test_kraken(self):
        # Bug 860516
        browser = Browser(self.marionette)
        browser.launch()

        print "Visit url %s" % self._start_page
        browser.go_to_url(self._start_page)
        time.sleep(2)

        print "Switch to the content of the page."
        browser.switch_to_content()
        time.sleep(2)

        print "Verify that the page is correctly loaded."
        self.verify_home_page()

        run_link = self.marionette.find_element(*self._run_locator)

        # wait 30s, to let the system settle.
        time.sleep(30)

        # start the benchmark
        run_link.tap()

        # Switch to the chrome, because the page will be automatically
        # redirected as soon as the benchmark is complete
        browser.switch_to_chrome()

        # wait 8 minutes, to let the becnhmark complete.
        print "Start benchmarking ..."
        time.sleep(8 * 60)
        browser.switch_to_content()
        self.verify_finished()

        self.print_results()

    def verify_home_page(self):
        self.wait_for_element_present(*self._run_locator)
        link = self.marionette.find_element(*self._run_locator)
        self.assertTrue(link.text == 'Begin',
                        'The kraken start page is not loaded.')

    def verify_finished(self):
        self.wait_for_element_present(*self._run_locator)
        link = self.marionette.find_element(*self._run_locator)
        self.assertTrue(link.text == 'Run Again',
                        'The kraken final page is not loaded.')

    def print_results(self):
        # Return a list of lines, as the full string is too large for
        # marionette.
        result = self.marionette.execute_script("""
          return document.getElementById('console').innerHTML
                   .replace(/<.?a[^>]*>/g, '').split('<br>')
        """)

        print "\n\nShell-like kraken results:"
        print "\n".join(result)
        print "End of shell-like results."
