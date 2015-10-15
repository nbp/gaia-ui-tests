# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import time
from marionette_driver import expected, By, Wait
from gaiatest import GaiaTestCase
from gaiatest.apps.search.app import Search


class TestBenchKraken(GaiaTestCase):

    _start_page = 'http://people.mozilla.com/~npierron/kraken/hosted/index.html'
    _run_locator = (By.CSS_SELECTOR, '#results > p > a')

    _console_locator = (By.ID, 'console')

    def setUp(self):
        GaiaTestCase.setUp(self)
        # Re-enable to bisect before Bug 1118891 (gaia).
        # self.apps.set_permission_by_url(Search.manifest_url, 'geolocation', 'deny')
        self.connect_to_local_area_network()
        # Never turn off the screen
        self.data_layer.set_setting('screen.timeout', 0)
        # Prevent tracking protection message from holding inputs for the browser.
        self.data_layer.set_bool_pref('privacy.trackingprotection.enabled', False)
        print ""

    def test_kraken(self):
        search = Search(self.marionette)
        search.launch()

        print "Visit url %s" % self._start_page
        browser = search.go_to_url(self._start_page)
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
        link = Wait(self.marionette).until(
            expected.element_present(*self._run_locator))
        Wait(self.marionette).until(
            expected.element_displayed(link))
        self.assertTrue(link.text == 'Begin',
                        'The kraken start page is not loaded.')

    def verify_finished(self):
        link = Wait(self.marionette).until(
            expected.element_present(*self._run_locator))
        Wait(self.marionette).until(
            expected.element_displayed(link))
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
