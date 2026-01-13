# -*- coding: utf-8 -*-
#
# Author: Ingelrest François (Francois.Ingelrest@gmail.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import gui

from gi.repository import Gtk

class BaseWin:
    """
        Add some functionalities to gtk.Window:
         * Automatically save and restore size
         * Hide the window instead of destroying it
         * Add a isVisible() function
         * Add a getWidget() function that acts like get_object()
    """

    def __init__(self, ui_file: str, win_id: str = 'win-main'):
        """ Constructor """
        self._wtr: Gtk.Builder = gui.createWTree(ui_file)
        # Load only the top-level container of the given .ui file
        self._win: Gtk.Window = self._wtr.get_object(win_id)
        # show all elements
        self._win.show_all()

    @property
    def title(self):
        return self._win.get_title()

    @title.setter
    def title(self, ttl: str):
        self._win.set_title(ttl)

    @property
    def position(self):
        return self._win.get_position()

    @position.setter
    def position(self, pos: int):
        self._win.set_position(pos)

    def attach(self, parent: type):
        self._win.set_transient_for(parent._win)
        self._win.set_position(gui.WIN_POS_CPARENT)

    def resize(self, w: int, h: int):
        """ Change window size """
        self._win.resize(w,h)

    def maximize(self, to_max = True):
        """ Maximize the window """
        self._win.maximized = to_max

    def getWidget(self, name: str):
        """ Return the widget with the given name """
        return self._wtr.get_object(name)

    def isVisible(self):
        """ Return True if the window is currently visible """
        return self._win.get_visible()

    def isMaximized(self):
        """ Return True if the window is maximized """
        return self._win.is_maximized()

    def show(self):
        """ Show the window if not visible, bring it to top otherwise """
        self._win.set_visible(True)

    def hide(self):
        """ Hide the window """
        self._win.set_visible(False)

    # Gtk Window Basic handlers
    def setOnResize(self, callback: callable):
        """ Save the new size of the dialog """
        self._win.connect('size-allocate', callback)

    def setOnStateChange(self, callback: callable):
        """ Save the new state of the dialog """
        self._win.connect('window-state-event', callback)

    def setOnClose(self, callback: callable):
        """ Hide the window instead of deleting it """
        self._win.connect('delete-event', callback)
