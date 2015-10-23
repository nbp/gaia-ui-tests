# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from marionette_driver import expected, By, Wait
from gaiatest import GaiaTestCase
from gaiatest.apps.system.app import System


class TestBenchOctane(GaiaTestCase):

    _start_page = 'http://people.mozilla.com/~npierron/octane-2.0/index.html'
    _run_octane_locator = (By.ID, 'run-octane')
    _last_benchmark_locator = (By.CSS_SELECTOR, '#Box-Typescript .p-result')
    _total_score_locator = (By.ID, 'main-banner')

    def setUp(self):
        GaiaTestCase.setUp(self)
        # Re-enable to bisect before Bug 1118891 (gaia).
        # self.apps.set_permission_by_url(Search.manifest_url, 'geolocation', 'deny')
        self.connect_to_local_area_network()
        # Never turn off the screen
        self.data_layer.set_setting('screen.timeout', 0)
        # Prevent tracking protection message from holding inputs for the browser.
        self.data_layer.set_bool_pref('privacy.trackingprotection.enabled', False)
        self.data_layer.set_bool_pref('privacy.trackingprotection.shown', True)
        print ""

    def test_octane(self):
        search = System(self.marionette).tap_search_bar()

        print "Visit url %s" % self._start_page
        browser = search.go_to_url(self._start_page)
        time.sleep(2)

        print "Switch to the content of the page."
        browser.switch_to_content()
        time.sleep(2)

        print "Verify that the page is correctly loaded."
        self.verify_home_page()

        print "Get octane button."
        run_button = Wait(self.marionette).until(
            expected.element_present(*self._run_octane_locator))

        # wait 30s, to let the system settle.
        print "wait 30 seconds."
        time.sleep(30)

        # run the benchmark
        print "tap button."
        run_button.tap()

        # wait 5 minutes, to let the becnhmark complete.
        print "Start benchmarking ..."
        time.sleep(8 * 60)
        self.verify_finished()

        self.print_results()

    def verify_home_page(self):
        tested = 0
        while True:
            try:
                Wait(self.marionette).until(expected.element_displayed(
                    Wait(self.marionette).until(expected.element_present(
                        *self._run_octane_locator))))
                break
            except:
                tested += 1
                if tested >= 5:
                    raise

    def verify_finished(self):
        result = Wait(self.marionette).until(
            expected.element_present(*self._last_benchmark_locator))
        Wait(self.marionette).until(
            expected.element_displayed(result))
        self.assertTrue(result.text.isdigit(), 'Benchmark is still running?')

    def print_results(self):
        result = self.marionette.execute_script("""
          var res = document.getElementsByClassName('p-result');
          var obj = [];
          var name, score, hasBad;
          for (var i = 0; i < res.length; i++) {
            name = res[i].id.slice(7); // Result-*
            score = res[i].textContent | 0; // ... Or 123
            if (score == 0)
              hasBad = true;
            else
              obj.push({"name": name, "score": score});
          }
          if (!hasBad) {
            obj.push({
              "name": "Score",
              "score": document.getElementById('main-banner')
                          .textContent.split(': ')[1] | 0
            });
          }
          return obj;
        """)

        print "\n\nShell-like octane results:"
        for i in result:
            print "%s: %d" % (i['name'], i['score'])
        print "End of shell-like results."
