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

from gi.repository import Gtk, Gdk
from tools.prefs   import UserPrefs
from gui.about     import MsgDialog
from gui.help      import HelpWin
from gui.window    import BaseWin
from tools         import prefs

from gui.preferences import PrefsWin

class MainWindow(MsgDialog, BaseWin):

    def __init__(self, p_usr: UserPrefs):
        """ Constructor """
        BaseWin.__init__(self, 'MainWindow.ui')

        mmini = self.getWidget('menu-mode-mini')
        mfull = self.getWidget('menu-mode-full')
        mlean = self.getWidget('menu-mode-lean')
        mnetb = self.getWidget('menu-mode-netbook')
        mplst = self.getWidget('menu-mode-playlist')
        m_prf = self.getWidget('menu-preferences')
        m_eql = self.getWidget('menu-equalizer')
        m_abo = self.getWidget('menu-about')
        m_hlp = self.getWidget('menu-help')
        m_qit = self.getWidget('menu-quit')
        m_pan = self.getWidget('pan-main')
        m_win = self.getWidget('win-main')

        p_usr.set_defaults(prefs.PFX_WINMAIN, [
            ('is-maximized', gui.DEFAULT_MAXIMIZED ),
            ('win-width'   , gui.DEFAULT_WIN_WIDTH ),
            ('win-height'  , gui.DEFAULT_WIN_HEIGHT),
            ('paned-pos'   , gui.DEFAULT_PANED_POS ),
            ('view-mode'   , gui.DEFAULT_VIEW_MODE ),
        ])
        self._opt = p_usr; self._hlp = None
        self._pan = m_pan; self._pfs = self._eql = None

        # Enable the right radio menu button
        vmode = p_usr.get_int('view-mode')

        if   vmode == gui.VIEW_MODE_FULL    : mfull.set_active(True)
        elif vmode == gui.VIEW_MODE_LEAN    : mlean.set_active(True)
        elif vmode == gui.VIEW_MODE_MINI    : mmini.set_active(True)
        elif vmode == gui.VIEW_MODE_NETBOOK : mnetb.set_active(True)
        elif vmode == gui.VIEW_MODE_PLAYLIST: mplst.set_active(True)

        # Restore the size and the state of the window
        if p_usr.get_bool('is-maximized'):
            m_win.maximize()

        i_width  = p_usr.get_int('win-width' )
        i_height = p_usr.get_int('win-height')
        i_pos    = p_usr.get_int('paned-pos' )

        m_win.resize(i_width, i_height)
        m_pan.set_position(i_pos)
        m_win.show_all()

        # Restore the view mode
        # We set the mode to VIEW_MODE_FULL in the preferences because the window is currently in this mode (initial startup state)
        p_usr.set('view-mode', gui.VIEW_MODE_FULL)
        self.setViewMode(vmode)

        # Restore once again the size (may have been modified while restoring the view mode)
        m_win.resize(i_width, i_height)
        m_pan.set_position(i_pos)

        # Finally connect the event handlers
        m_win.connect('delete-event'      , lambda *_: self.closeMain())
        m_win.connect('size-allocate'     , self._onResize)
        m_win.connect('window-state-event', self._onState)
        m_pan.connect('size-allocate'     , self._onSizeAlloc)

        mmini.connect('activate', self.onViewMode, gui.VIEW_MODE_MINI)
        mfull.connect('activate', self.onViewMode, gui.VIEW_MODE_FULL)
        mlean.connect('activate', self.onViewMode, gui.VIEW_MODE_LEAN)
        mnetb.connect('activate', self.onViewMode, gui.VIEW_MODE_NETBOOK)
        mplst.connect('activate', self.onViewMode, gui.VIEW_MODE_PLAYLIST)

        m_abo.connect('activate', lambda _: self.about())
        m_prf.connect('activate', lambda _: self.openPreferences())
        m_eql.connect('activate', lambda _: self.openEqualizer())
        m_hlp.connect('activate', lambda _: self.openHelp())
        m_qit.connect('activate', lambda _: self.closeMain())

    def setViewMode(self, mode: int):
        """ Change the view mode to the given one """
        pvmod = self._opt.get_int('view-mode')
        # Give up if the new mode is the same as the current one
        if pvmod == mode:
            return
        # First restore the initial window state (e.g., VIEW_MODE_FULL)
        if   pvmod == gui.VIEW_MODE_LEAN:     self._setLeanMode   (unset=True)
        elif pvmod == gui.VIEW_MODE_MINI:     self._setFullMode   (unset=True, mini=True)
        elif pvmod == gui.VIEW_MODE_NETBOOK:  self._setNetbookMode(unset=True)
        elif pvmod == gui.VIEW_MODE_PLAYLIST: self._setFullMode   (unset=True)
        # Now we can switch to the new mode
        if    mode == gui.VIEW_MODE_LEAN:     self._setLeanMode()
        elif  mode == gui.VIEW_MODE_MINI:     self._setFullMode(mini=True)
        elif  mode == gui.VIEW_MODE_NETBOOK:  self._setNetbookMode()
        elif  mode == gui.VIEW_MODE_PLAYLIST: self._setFullMode()
        # Save the new mode
        self._opt.set('view-mode', mode)

    # --== Lean Mode ==--
    def _setLeanMode(self, unset = False):
        """ Switch from lean mode to full mode """
        trackList = self.getWidget('box-btn-tracklist')
        # ~~
        trackList.set_visible(unset is True)

    # --== Mini Mode ==--
    def _setFullMode(self, unset = False, mini = False):
        """ Switch from mini mode to full mode """
        trackList = self.getWidget('box-btn-tracklist')
        trkScroll = self.getWidget('scrolled-tracklist')
        statusBar = self.getWidget('statusbar')
        panMain   = self.getWidget('pan-main')
        panChild1 = panMain.get_child1()
        ( iw,ih ) = self._win.get_size()
        fHeight   = self._opt.get_int('full-win-height')

        if mini : ih  = fHeight if unset else -1
        if unset: iw += panMain.get_position()
        else    : iw -= panMain.get_position()

        statusBar.set_visible(unset is True and mini is True)
        trkScroll.set_visible(unset is True and mini is True)
        panChild1.set_visible(unset is True)
        trackList.set_visible(unset is True)
        # Do only one resize(), because intermediate get_size() don't return the correct size until the event queue has been processed by GTK
        self._win.resize(iw, ih)

    # --== Lean Mode ==--
    def _setNetbookMode(self, unset = False):
        """ Switch from netbook mode to full mode """
        trackList = self.getWidget('box-btn-tracklist')
        trackInfo = self.getWidget('box-trkinfo')
        boxSlider = self.getWidget('box-slider')
        boxExplor = self.getWidget('box-explorer')
        ctrlPanel = self.getWidget('box-ctrl-panel')
        ctrlBtns1 = self.getWidget('box-ctrl-buttons-1')
        ctrlBtns2 = self.getWidget('box-ctrl-buttons-2')
        boxCmbExp = self.getWidget('box-combo-explorer')
        combExplr = self.getWidget('combo-explorer')

        if not unset:
            boxSlider.reparent(boxExplor)
            combExplr.reparent(ctrlBtns2); b1 = -1
            ctrlBtns2.reparent(boxCmbExp); a2 = -1
        else:
            boxSlider.reparent(ctrlPanel)
            ctrlBtns2.reparent(ctrlBtns1); b1 = 45
            combExplr.reparent(boxCmbExp); a2 = 20

        trackList.set_visible(unset is True)
        trackInfo.set_visible(unset is True)
        boxSlider.set_size_request(-1, a2)
        combExplr.set_size_request(b1, -1)

        if not unset:
            boxExplor.child_set_property(boxSlider, 'expand', False)


    # --== GTK Handlers ==--


    def _onResize(self, win, rect):
        """ Save the new size of the window """
        # The first status label gets more or less a third of the window's width
        hbox = self._wtr.get_object('hbox-status1')
        hbox.set_size_request(rect.width / 3 + 15, -1)

        # Save size and maximized state
        if win is not None and not win.get_state() == Gdk.WindowState.MAXIMIZED:
            vmode = self._opt.get('view-mode')

            if vmode != gui.VIEW_MODE_MINI:
                self._opt.set('full-win-height', rect.height)

            self._opt.set('win-width',  rect.width )
            self._opt.set('win-height', rect.height)


    def _onState(self, win: Gtk.Window, e: Gdk.EventWindowState):
        """ Save the new state of the window """
        self._opt.set('is-maximized', e.new_window_state == Gdk.WindowState.MAXIMIZED)

    def onViewMode(self, item, mode):
        """ Wrapper for setViewMode() """
        if item.get_active():
            self.setViewMode(mode)


    def _onSizeAlloc(self, item, rect=None):
        self._opt.set('paned-pos', self._pan.get_position())

    def startMain(self):
        """ Starts main loop and present the main window """
        Gtk.main()
        
        return False

    def closeMain(self):
        """ Quit main loop sequence, that will itself destroy all windows """
        Gtk.main_quit()

    def openPreferences(self):
        """ Show preferences """
        if self._pfs is None:
            self._pfs = PrefsWin()
            self._pfs.attach(self)
        # ~~
        self._pfs.show()

    def openEqualizer(self):
        """ Show equalizer """
        if self._eql is None:
            self._eql = BaseWin('Equalizer.ui')
            self._eql.attach(self)
        # ~~
        self._eql.show()

    def openHelp(self):
        """ Show help page in the new window """
        if self._hlp is None:
            self._hlp = HelpWin()
            self._hlp.attach(self)
        # ~~
        self._hlp.show()
