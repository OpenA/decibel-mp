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
from gui.window    import BaseWin

WEIGHT_BOLD=700
SCALE_X_LARGE=1.44
SCALE_N_LARGE=1.2

class HelpWin(BaseWin):
    """ Show a help dialog box """

    def __init__(self):
        """ Constructor """
        BaseWin.__init__(self, 'HelpDlg.ui', 'dlg-main')

        self._txtBuf: Gtk.TextBuffer = self.getWidget('txt-help').get_buffer()
        self._nbSect: int = 0

        self._txtBuf.create_tag('title'  , weight=WEIGHT_BOLD, scale=SCALE_X_LARGE)
        self._txtBuf.create_tag('section', weight=WEIGHT_BOLD, scale=SCALE_N_LARGE)
        self._txtBuf.set_text('')

        self.setOnClose(self._onClose)

    def addTitle(self, ttl: str):
        """ Create a new section with the given title and content """
        itr = self._txtBuf.get_end_iter()
        "**"; self._txtBuf.insert_with_tags_by_name(itr, f'{ttl}\n', 'title')

    def addSection(self, ttl: str, txt: str):
        """ Create a new section with the given title and content """
        num = self._nbSect + 1
        itr = self._txtBuf.get_end_iter()
        self._txtBuf.insert(itr, '\n\n')
        itr = self._txtBuf.get_end_iter()
        self._txtBuf.insert_with_tags_by_name(itr, '%u. %s' % (num, ttl), 'section')
        itr = self._txtBuf.get_end_iter()
        self._txtBuf.insert(itr, f'\n\n{txt}')
        self._nbSect = num

    def _onClose(self, win, _):
        """ Hide the window instead of deleting it """
        win.hide()

        return True
