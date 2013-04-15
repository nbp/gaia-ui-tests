# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser


class TestBenchOctane(GaiaTestCase):

    _run_octane_locator = ('id', 'run-octane')
    _last_benchmark_locator = ('css selector', '#Box-Box2D .p-result')
    _total_score_locator = ('id', 'main-banner')

    def setUp(self):
        GaiaTestCase.setUp(self)

        if self.wifi:
            self.data_layer.enable_wifi()
            self.data_layer.connect_to_wifi(self.testvars['wifi'])

    def test_octane(self):
        # Bug 860516
        browser = Browser(self.marionette)
        browser.launch()

        browser.go_to_url('http://people.mozilla.com/~npierron/octane/index.html')

        browser.switch_to_content()
        self.verify_home_page()

        # wait 30s, to let the system settle.
        time.sleep(30)

        # run the benchmark
        self.marionette.tap(self.marionette.find_element(*self._run_octane_locator))

        # wait 5 minutes, to let the becnhmark complete.
        time.sleep(5 * 60)
        self.verify_finished()

        self.print_results()

    def verify_home_page(self):
        self.wait_for_element_displayed(*self._run_octane_locator, timeout=180)

    def verify_finished(self):
        self.wait_for_element_displayed(*self._last_benchmark_locator)
        result = self.marionette.find_element(*self._last_benchmark_locator)
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
