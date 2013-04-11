# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
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
        # https://github.com/mozilla/gaia-ui-tests/issues/450
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

        result = self.collect_results()
        print json.dumps(result, indent=2, separators=(',', ': '))

    def verify_home_page(self):
        self.wait_for_element_present(*self._run_octane_locator)
        link = self.marionette.find_element(*self._run_octane_locator)
        self.assertTrue(link.is_displayed, 'The octane page is not rendered.')

    def verify_finished(self):
        self.wait_for_element_present(*self._last_benchmark_locator)
        result = self.marionette.find_element(*self._last_benchmark_locator)
        self.assertTrue(result.is_displayed, '(1) still running?')
        self.assertTrue(result.text.isdigit(), '(2) still running?')

    def collect_results(self):
        return self.marionette.execute_script("""
          var res = document.getElementsByClassName('p-result');
          var obj = {};
          var name, score;
          for (var i = 0; i < res.length; i++) {
            name = res[i].id.slice(7); // Result-*
            score = res[i].textContent | 0; // ... Or 123
            obj[name] = score;
          }
          obj.total = document.getElementById('main-banner')
                        .textContent.split(': ')[1] | 0;
          return obj;
        """)
