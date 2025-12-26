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

from gi.repository import Gdk
from tools.prefs   import UserPrefs
from gui.about     import MsgDialog
from tools         import prefs


class MainWindow(MsgDialog):

    def __init__(self, p_usr: UserPrefs):
        """ Constructor """
        wtree =  gui.createWTree('MainWindow.ui')
        mmini = wtree.get_object('menu-mode-mini')
        mfull = wtree.get_object('menu-mode-full')
        mlean = wtree.get_object('menu-mode-lean')
        mnetb = wtree.get_object('menu-mode-netbook')
        mplst = wtree.get_object('menu-mode-playlist')
        mpref = wtree.get_object('menu-preferences')
        mabut = wtree.get_object('menu-about')
        mhelp = wtree.get_object('menu-help')
        mquit = wtree.get_object('menu-quit')
        m_pan = wtree.get_object('pan-main')
        m_win = wtree.get_object('win-main')

        p_usr.set_defaults(prefs.PFX_WINMAIN, [
            ('is-maximized', gui.DEFAULT_MAXIMIZED ),
            ('win-width'   , gui.DEFAULT_WIN_WIDTH ),
            ('win-height'  , gui.DEFAULT_WIN_HEIGHT),
            ('paned-pos'   , gui.DEFAULT_PANED_POS ),
            ('view-mode'   , gui.DEFAULT_VIEW_MODE ),
        ])
        super(MsgDialog, self).__init__()

        self._wtr = wtree; self._pan = m_pan
        self._opt = p_usr; self._win = m_win

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
        m_win.connect('delete-event'      , self._onQuit)
        m_win.connect('size-allocate'     , self._onResize)
        m_win.connect('window-state-event', self._onState)
        m_pan.connect('size-allocate'     , self._onSizeAlloc)

        mmini.connect('activate', self.onViewMode, gui.VIEW_MODE_MINI)
        mfull.connect('activate', self.onViewMode, gui.VIEW_MODE_FULL)
        mlean.connect('activate', self.onViewMode, gui.VIEW_MODE_LEAN)
        mnetb.connect('activate', self.onViewMode, gui.VIEW_MODE_NETBOOK)
        mplst.connect('activate', self.onViewMode, gui.VIEW_MODE_PLAYLIST)

        mhelp.connect('activate', self.onHelp)
        mabut.connect('activate', self.onAbout)
        mpref.connect('activate', self.onShowPreferences)
        mquit.connect('activate', self._onQuit)

    def setViewMode(self, mode):
        """ Change the view mode to the given one """
        currMode = self._opt.get_int('view-mode')

        # Give up if the new mode is the same as the current one
        if currMode == mode:
            return

        requestedSize = self._win.get_size()

        # First restore the initial window state (e.g., VIEW_MODE_FULL)
        if   currMode == gui.VIEW_MODE_LEAN:     requestedSize = self.__fromModeLean(requestedSize)
        elif currMode == gui.VIEW_MODE_MINI:     requestedSize = self.__fromModeMini(requestedSize)
        elif currMode == gui.VIEW_MODE_NETBOOK:  requestedSize = self.__fromModeNetbook(requestedSize)
        elif currMode == gui.VIEW_MODE_PLAYLIST: requestedSize = self.__fromModePlaylist(requestedSize)

        # Now we can switch to the new mode
        if   mode == gui.VIEW_MODE_LEAN:     requestedSize = self.__toModeLean(requestedSize)
        elif mode == gui.VIEW_MODE_MINI:     requestedSize = self.__toModeMini(requestedSize)
        elif mode == gui.VIEW_MODE_NETBOOK:  requestedSize = self.__toModeNetbook(requestedSize)
        elif mode == gui.VIEW_MODE_PLAYLIST: requestedSize = self.__toModePlaylist(requestedSize)

        # Do only one resize(), because intermediate get_size() don't return the correct size until the event queue has been processed by GTK
        self._win.resize(requestedSize[0], requestedSize[1])

        # Save the new mode
        self._opt.set('view-mode', mode)


    # --== Lean Mode ==--

    def __fromModeLean(self, requestedSize):
        """ Switch from lean mode to full mode """
        self._wtr.get_object('box-btn-tracklist').show()

        return requestedSize


    def __toModeLean(self, requestedSize):
        """ Switch from full mode to lean mode """
        self._wtr.get_object('box-btn-tracklist').hide()

        return requestedSize


    # --== Netbook Mode ==--

    def __fromModeNetbook(self, requestedSize):
        """ Switch from netbook mode to full mode """
        self._wtr.get_object('box-trkinfo').show()
        self._wtr.get_object('box-btn-tracklist').show()

        slider           = self._wtr.get_object('box-slider')
        ctrlPanel        = self._wtr.get_object('box-ctrl-panel')
        ctrlButtons      = self._wtr.get_object('box-ctrl-buttons-2')
        comboExplorer    = self._wtr.get_object('combo-explorer')
        ctrlButtonsBox   = self._wtr.get_object('box-ctrl-buttons-1')
        boxComboExplorer = self._wtr.get_object('box-combo-explorer')

        slider.reparent(ctrlPanel)
        ctrlButtons.reparent(ctrlButtonsBox)
        comboExplorer.reparent(boxComboExplorer)

        slider.set_size_request(-1, -1)
        comboExplorer.set_size_request(-1, -1)

        return requestedSize


    def __toModeNetbook(self, requestedSize):
        """ Switch from full mode to netbook mode """
        self._wtr.get_object('box-trkinfo').hide()
        self._wtr.get_object('box-btn-tracklist').hide()

        slider           = self._wtr.get_object('box-slider')
        boxExplorer      = self._wtr.get_object('box-explorer')
        ctrlButtons      = self._wtr.get_object('box-ctrl-buttons-2')
        comboExplorer    = self._wtr.get_object('combo-explorer')
        boxComboExplorer = self._wtr.get_object('box-combo-explorer')

        slider.reparent(boxExplorer)
        comboExplorer.reparent(ctrlButtons)
        ctrlButtons.reparent(boxComboExplorer)

        slider.set_size_request(-1, 20)
        comboExplorer.set_size_request(45, -1)
        boxExplorer.child_set_property(slider, 'expand', False)

        return requestedSize


    # --== Mini Mode ==--

    def __fromModeMini(self, requestedSize):
        """ Switch from mini mode to full mode """
        self._pan.get_child1().show()
        self._wtr.get_object('statusbar').show()
        self._wtr.get_object('box-btn-tracklist').show()
        self._wtr.get_object('scrolled-tracklist').show()

        (winWidth, winHeight) = requestedSize

        return (winWidth + self._pan.get_position(), self._opt.get_int('full-win-height'))


    def __toModeMini(self, requestedSize):
        """ Switch from full mode to mini mode """
        self._pan.get_child1().hide()
        self._wtr.get_object('statusbar').hide()
        self._wtr.get_object('box-btn-tracklist').hide()
        self._wtr.get_object('scrolled-tracklist').hide()

        (winWidth, winHeight) = requestedSize

        return (winWidth - self._pan.get_position(), 1)


    # --== Playlist Mode ==--

    def __fromModePlaylist(self, requestedSize):
        """ Switch from playlist mode to full mode """
        self._pan.get_child1().show()
        self._wtr.get_object('box-btn-tracklist').show()

        (winWidth, winHeight) = requestedSize

        return (winWidth + self._pan.get_position(), winHeight)


    def __toModePlaylist(self, requestedSize):
        """ Switch from full mode to playlist mode """
        self._pan.get_child1().hide()
        self._wtr.get_object('box-btn-tracklist').hide()

        (winWidth, winHeight) = requestedSize

        return (winWidth - self._pan.get_position(), winHeight)


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

    def _onQuit(self, item, data=None):
        """ Use our own quit sequence, that will itself destroy the window """

        self._opt.save()
        gui.atExit()

        return True


    def onShowPreferences(self, item):
        """ Show preferences """

        gui.preferences.show()

    def onInterrupt():
        """ Handler for interrupt signals e.g., Ctrl-C """

        # TODO: handle errors

    def onAbout(self, item):
        """ Show the about dialog box """

        self.about()


    def onHelp(self, item):
        """ Show help page in the web browser """

        # TODO: open help file
