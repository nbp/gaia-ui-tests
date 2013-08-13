# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.everythingme.app import EverythingMe


class TestEverythingMeSearch(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        self.connect_to_network()
        self.everythingme = EverythingMe(self.marionette)

    def test_launch_everything_me_search(self):
        # Tests a search with a common string.
        # Asserts that the title and shortcuts are listed

        test_string = u'skyfall'
        self.everythingme.go_to_everything_me()

        self.everythingme.wait_for_search_box_displayed()
        self.everythingme.type_into_search_box(test_string)
        self.assertIn(test_string, self.everythingme.search_title)

        self.everythingme.wait_for_app_icons_displayed()
        self.assertGreater(self.everythingme.apps_count, 0, 'No apps found')
