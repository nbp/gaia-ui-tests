# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base


class Messages(Base):

    name = 'Messages'
    _summary_header_locator = ('css selector', "h1[data-l10n-id='messages']")
    _create_new_message_locator = ('id', 'icon-add')

    def launch(self):
        Base.launch(self)
        self.wait_for_element_displayed(*self._summary_header_locator)

    def tap_create_new_message(self):
        self.marionette.find_element(*self._create_new_message_locator).tap()
        from gaiatest.apps.messages.regions.new_message import NewMessage
        return NewMessage(self.marionette)
