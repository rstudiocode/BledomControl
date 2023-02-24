# window.py
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
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gio, Gtk, GLib, Adw


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, loop, **kwargs):
        super().__init__(**kwargs)
        self.set_default_size(640, 480)
        self.set_title("My App")


        # Create title bar with about button
        header_bar = Gtk.HeaderBar()
        self.set_titlebar(header_bar)

        # Create a new menu, containing that action
        menu = Gio.Menu.new()
        menu.append("Do Something", "win.something")  # Or you would do app.something if you had attached the
        # action to the application

        # Create a popover
        self.popover = Gtk.PopoverMenu()  # Create a new popover menu
        self.popover.set_menu_model(menu)

        # Create a menu button
        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")  # Give it a nice icon
        header_bar.pack_end(self.hamburger)

        # Set app name
        GLib.set_application_name("My App")

        # Create an action to run a *show about dialog* function we will create
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about_action)
        self.add_action(action)

        menu.append("About", "win.about")

        # Create main box container
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.main_box)
        self.main_box.set_spacing(10)
        self.main_box.set_margin_top(10)
        self.main_box.set_margin_bottom(10)
        self.main_box.set_margin_start(10)
        self.main_box.set_margin_end(10)

        # Create color chooser in center of window
        color_chooser = Gtk.ColorChooserWidget()
        self.main_box.append(color_chooser)

        # Create dropdown menu with options
        dropdown_menu = Gtk.ComboBoxText()
        dropdown_menu.append_text("Option 1")
        dropdown_menu.append_text("Option 2")
        dropdown_menu.append_text("Option 3")
        self.main_box.append(dropdown_menu)

        # Create refresh button with icon under color chooser
        refresh_button = Gtk.Button()
        refresh_icon = Gio.ThemedIcon(name="view-refresh-symbolic")
        refresh_image = Gtk.Image.new_from_gicon(refresh_icon)
        refresh_button.set_child(refresh_image)
        self.main_box.append(refresh_button)


    def on_about_action(self, widget, _):
        about = Gtk.AboutDialog()

        about.set_authors(["Artem Sukhanov"])
        about.set_copyright("Copyright 2023 by Artem Sukhanov")
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_website("http://example.com")
        about.set_website_label("My Website")
        about.set_version("1.0")
        about.set_logo_icon_name("org.example.example")  # The icon will need to be added to appropriate location
        # E.g. /usr/share/icons/hicolor/scalable/apps/org.example.example.svg

        about.show()
