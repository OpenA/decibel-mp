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

from tools.consts  import ICR_EXIT, ICR_MINIT, NO_TITLE, NO_ARTIST
from gi.repository import Gtk
from gui.about     import MsgDialog

class MainWinApp(Gtk.Application, MsgDialog):
    """
        Add some functionalities to gtk.Window:
         * Automatically save and restore size
         * Hide the window instead of destroying it
         * Add a isVisible() function
         * Add a getWidget() function that acts like get_object()
    """

    def __init__(self, app_id: str, app_flags: int):
        """ Constructor """
        super().__init__(application_id=app_id, flags=app_flags)
        # Load only the top-level container of the given .ui file
        self._tre: Gtk.Builder   = None
        self._win: Gtk.Window    = None
        self._hdb: Gtk.HeaderBar = None
        # show all elements
        self._played = self._paused = False

    def do_activate(self):
        # Access a resource using its full resource path (prefix + filename)
        m_tre = self._tre = Gtk.Builder.new_from_resource("/org/decibel-mp/gtk/MainWindow.ui")
        m_win = self._win = m_tre.get_object("win_main")
        h_bar = self._hdb = m_tre.get_object("hd_bar")

        c_prv = m_tre.get_object("ctrl_btn_prev"); b_eqz = m_tre.get_object("menu_btn_eqlz")
        c_nxt = m_tre.get_object("ctrl_btn_next"); b_qut = m_tre.get_object("menu_btn_quit")
        c_ply = m_tre.get_object("ctrl_btn_play"); b_abt = m_tre.get_object("menu_btn_about")
        c_stp = m_tre.get_object("ctrl_btn_stop"); b_xxx = m_tre.get_object("act1_btn_close")

        self.add_window(m_win)

        h_bar.set_subtitle(NO_ARTIST)
        h_bar.set_title   (NO_TITLE)
        m_win.present()
        b_abt.connect('clicked', lambda _: self.about())
        b_qut.connect('clicked', lambda _: self.quit())
        b_xxx.connect('clicked', lambda _: self.quit() if not self._played else self.minimize())
        c_ply.connect('clicked', lambda _: self.setStatusPlay(played=True, paused=not self._paused))
        c_stp.connect('clicked', lambda _: self.setStatusPlay())

    @property
    def state(self):
        """ Return window state flags """
        return self._win.get_state()

    @property
    def title(self):
        return self._hdb.get_title()

    @title.setter
    def title(self, ttl: str):
        self._hdb.set_title(ttl)

    @property
    def artist(self):
        return self._hdb.get_subtitle()

    @artist.setter
    def artist(self, ttl: str):
        self._hdb.set_subtitle(ttl)

    def minimize(self):
        """ Minimize the window """
        self._win.iconify()

    def resize(self, w: int, h: int):
        """ Change window size """
        self._win.resize(w,h)

    def maximize(self, to_max = True):
        """ Maximize the window """
        self._win.maximized = to_max

    def getWidget(self, name: str):
        """ Return the widget with the given name """
        return self._tre.get_object(name)

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
    def onResizeChange(self, callback: callable):
        """ Save the new size of the dialog """
        self._win.connect('size-allocate', callback)

    def onStateChange(self, callback: callable):
        """ Save the new state of the dialog """
        self._win.connect('window-state-event', callback)

    def setStatusPlay(self, played = False, paused = False):
        """ Hide the window instead of deleting it """
        btn_play  = self.getWidget('ctrl_btn_play')
        btn_close = self.getWidget('act1_btn_close')
        ico_play  = self.getWidget('mp-play' ); self._played = played
        ico_pause = self.getWidget('mp-pause'); self._paused = paused

        btn_play .set_image(ico_play if not paused or  not played else ico_pause)
        btn_close.set_label(ICR_EXIT if not paused and not played else ICR_MINIT)
