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

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from tools         import consts

# --- View modes
(
    VIEW_MODE_FULL,
    VIEW_MODE_LEAN,
    VIEW_MODE_MINI,
    VIEW_MODE_PLAYLIST,
    VIEW_MODE_NETBOOK,
) = range(5)

DEFAULT_VIEW_MODE  = VIEW_MODE_FULL
DEFAULT_PANED_POS  = 320
DEFAULT_WIN_WIDTH  = 930
DEFAULT_WIN_HEIGHT = 568
DEFAULT_MAXIMIZED  = False

def createWTree(file: str):
    """ Load the given Glade file and return the tree of widgets """
    tree = Gtk.Builder()
    ____ = tree.add_from_file(consts.APP_UI_DIR + file)
    return tree

def startUp():
    """
        Perform all the initialization stuff that is not mandatory to display the window
        This function should be called within the GTK main loop, once the window has been displayed
    """
    Gtk.main()

def atExit():
    """ Final function, called just before exiting the Python interpreter """
    Gtk.main_quit()
