# main.py
#
# Copyright 2023 Artem Sukhanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later


import asyncio
import logging
import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Gio, Gtk, Adw
from main_window import MainWindow

Adw.init()


logger = logging.getLogger('MainApp')
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)


class Application(Adw.Application):
    def __init__(self):
        super().__init__(application_id='space.stakancheck.BledomControl',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('about', self.on_about_action)

    def do_activate(self):
        loop = asyncio.new_event_loop()

        win = self.props.active_window
        if not win:
            win = MainWindow(application=self, loop=loop)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def on_preferences_action(self, action, param):
        logger.info('Preferences...')

    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow.new()
        dialog.set_transient_for(parent=self.get_active_window())
        dialog.set_application_name('Bledom Control')
        dialog.set_version('0.0.1')
        dialog.set_developer_name('Artem Sukhanov (stakancheck)')
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_comments('App for control bluetooth led devices')
        dialog.set_website('https://github.com/stakancheck/BledomControl')
        dialog.set_issue_url("https://github.com/stakancheck/BledomControl/issues")
        dialog.set_copyright('© 2023 Artem Sukhanov (stakancheck)')
        dialog.set_developers(['stakancheck https://github.com/stakancheck'])
        dialog.set_application_icon('help-about-symbolic')
        dialog.present()

    def exit_app(self, action, param):
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)


def main():
    app = Application()
    app.run(sys.argv)


if __name__ == '__main__':
    main()
