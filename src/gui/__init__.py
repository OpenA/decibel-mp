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

from gi.repository import Gtk, Gio

DEFAULT_APP_FLAGS  = Gio.ApplicationFlags.FLAGS_NONE
DEFAULT_PANED_POS  = 320
DEFAULT_WIN_WIDTH  = 930
DEFAULT_WIN_HEIGHT = 568
DEFAULT_MAXIMIZED  = False

def register_resource(ui_file: str):
    """ Load the given Glade file and return the tree of widgets """
    res = Gio.Resource.load(ui_file)
    ___ = Gio.resources_register(res)
