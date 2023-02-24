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
gi.require_version(namespace='Adw', version='1')

from gi.repository import Gio, Gtk, GLib, Adw

Adw.init()


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, loop, **kwargs):
        super().__init__(**kwargs)

        self.app_name = 'Bledom Control'
        self.loop = loop

        self.set_default_size(640, 480)
        self.set_title(title=self.app_name)

        # Set app name
        GLib.set_application_name(self.app_name)

        # Create title bar with about button
        header_bar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=header_bar)

        # Create a new menu, containing that action
        menu = Gio.Menu.new()
        menu.append('Preferences', 'app.preferences')
        menu.append("About", "app.about")

        # Create a popover
        self.popover = Gtk.PopoverMenu()  # Create a new popover menu
        self.popover.set_menu_model(menu)

        # Create a menu button
        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")  # Give it a nice icon
        header_bar.pack_end(self.hamburger)

        # Create source box container
        source_box = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_child(child=source_box)

        # Create main box container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.set_spacing(10)
        main_box.set_margin_top(10)
        main_box.set_margin_bottom(10)
        main_box.set_margin_start(10)
        main_box.set_margin_end(10)
        source_box.append(main_box)

        devices_continer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        devices_continer.append(Gtk.Label.new(str='Choose device'))
        devices_chooser_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        # Create refresh button
        refresh_button = Gtk.Button()
        refresh_icon = Gio.ThemedIcon(name="view-refresh-symbolic")
        refresh_image = Gtk.Image.new_from_gicon(refresh_icon)
        refresh_button.set_child(refresh_image)
        devices_chooser_container.append(refresh_button)

        # Create dropdown menu with options
        dropdown_menu = Gtk.ComboBoxText()
        dropdown_menu.append_text("Option 1")
        dropdown_menu.append_text("Option 2")
        dropdown_menu.append_text("Option 3")
        devices_chooser_container.append(dropdown_menu)
        devices_continer.append(devices_chooser_container)
        main_box.append(devices_continer)

        # Create color chooser in center of window
        color_chooser = Gtk.ColorChooserWidget.new()
        color_chooser.set_use_alpha(False)
        main_box.append(color_chooser)
