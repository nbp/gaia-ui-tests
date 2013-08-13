# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.everythingme.app import EverythingMe


class TestEverythingMeLaunchApp(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        self.connect_to_network()
        self.everythingme = EverythingMe(self.marionette)

    def test_launch_everything_me_app(self):
        # https://github.com/mozilla/gaia-ui-tests/issues/69

        app_name = 'Twitter'
        self.everythingme.go_to_everything_me()

        self.everythingme.wait_for_categories_to_load()
        self.assertGreater(self.everythingme.categories_count, 0, 'No shortcut categories found')
        self.everythingme.tap_category('social')

        self.everythingme.wait_for_app_icons_displayed()
        self.everythingme.tap_app_icon(app_name)

        self.assertIn(app_name, self.marionette.title)
