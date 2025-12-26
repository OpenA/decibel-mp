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

from gi.repository import Gtk

from tools   import consts
from gettext import gettext as _


class MsgDialog:

    def __init__(self, win: Gtk.Window = None):
        self._win = win

    # Functions used to display various message boxes
    def info(self, inf_p: str, inf_s: str = None):
        """ Show a generic message box """
        dlg = Gtk.MessageDialog( modal = True,
                          message_type = Gtk.MessageType.INFO,
                         transient_for = self._win,
                                markup = inf_p)
        if inf_s != None:
            dlg.format_secondary_markup(inf_s)
        dlg.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        dlg.run()
        dlg.destroy()

    def error(self, err_p: str, err_s: str = None):
        """ Show a generic message box """
        dlg = Gtk.MessageDialog( modal = True,
                          message_type = Gtk.MessageType.ERROR,
                         transient_for = self._win,
                                  text = err_p)
        if err_s != None:
            dlg.format_secondary_text(err_s)
        dlg.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        dlg.run()
        dlg.destroy()

    def question(self, que_p: str, que_s: str = None):
        """ Show a generic message box """
        dlg = Gtk.MessageDialog( modal = True,
                          message_type = Gtk.MessageType.QUESTION,
                         transient_for = self._win,
                                  text = que_p)
        if que_s != None:
            dlg.format_secondary_text(que_s)
        dlg.add_button(Gtk.STOCK_YES, Gtk.ResponseType.OK)
        dlg.add_button(Gtk.STOCK_NO , Gtk.ResponseType.CANCEL)
        res = dlg.run() is Gtk.ResponseType.OK
        ___ = dlg.destroy()
        return res

    def about(self):
        """ Show an about dialog box """
        dlg = Gtk.AboutDialog()
        
        if self._win is not None:
            dlg.set_transient_for(self._win)

        # Set credit information
        dlg.set_name(consts.APP_NAME)
        dlg.set_comments('...And Music For All')
        dlg.set_version(consts.APP_VERSION)
        dlg.set_website(consts.APP_HOMEURL)
        dlg.set_website_label(consts.APP_HOMEURL)
        dlg.set_translator_credits(_('translator-credits'))

        dlg.set_artists([
            _('Decibel Audio Player icon:'),
            '    Sébastien Durel <sebastien.durel@gmail.com>',
            '',
            _('Other icons:'),
            '    7 icon pack <www.tehkseven.net>',
            '    Tango project <tango.freedesktop.org>',
        ])

        dlg.set_authors([
            _('Developer:'),
            '    François Ingelrest <Francois.Ingelrest@gmail.com>',
            '',
            _('Thanks to:'),
            '    Emilio Pozuelo Monfort <pochu@ubuntu.com>',
        ])

        # Set logo
        #dlg.set_logo(gtk.gdk.pixbuf_new_from_file(consts.fileImgIcon128))

        # Load the licence from the disk if possible
        #if os.path.isfile(consts.fileLicense):
        #    dlg.set_license(open(consts.fileLicense).read())
        #    dlg.set_wrap_license(True)

        dlg.run()
        dlg.destroy()
