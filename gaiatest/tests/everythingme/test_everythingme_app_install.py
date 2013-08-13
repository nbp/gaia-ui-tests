# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest import GaiaTestCase
from gaiatest.apps.everythingme.app import EverythingMe


class TestEverythingMeInstallApp(GaiaTestCase):

    # Homescreen locators
    _homescreen_frame_locator = (By.CSS_SELECTOR, 'div.homescreen > iframe')
    _homescreen_icon_locator = (By.CSS_SELECTOR, 'li.icon[aria-label="%s"]')

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        self.connect_to_network()
        self.everythingme = EverythingMe(self.marionette)

    def test_installing_everything_me_app(self):
        # https://github.com/mozilla/gaia-ui-tests/issues/67

        self.everythingme.go_to_everything_me()

        self.everythingme.wait_for_categories_to_load()
        self.assertGreater(self.everythingme.categories_count, 0, 'No shortcut categories found')
        self.everythingme.categories[0].tap()

        self.everythingme.wait_for_app_icons_displayed()
        app_name = self.everythingme.app_icons[0].tap_to_install()

        # return to home screen
        hs_frame = self.marionette.find_element(*self._homescreen_frame_locator)
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")
        self.marionette.switch_to_frame(hs_frame)

        self.assertTrue(self.is_app_installed(app_name),
                        'The app %s was not found to be installed on the home screen.' % app_name)

    def is_app_installed(self, app_name):
        """Checks whether app is installed"""
        is_installed = False
        while self._homescreen_has_more_pages:
            self._go_to_next_page()
            if self.is_element_displayed(self._homescreen_icon_locator[0], self._homescreen_icon_locator[1] % app_name):
                is_installed = True
                break

        return is_installed

    def _go_to_next_page(self):
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToNextPage()')

    @property
    def _homescreen_has_more_pages(self):
        # the naming of this could be more concise when it's in an app object!
        return self.marionette.execute_script("""
        var pageHelper = window.wrappedJSObject.GridManager.pageHelper;
        return pageHelper.getCurrentPageNumber() < (pageHelper.getTotalPagesNumber() - 1);""")
