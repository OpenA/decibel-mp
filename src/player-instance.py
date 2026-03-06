#!/usr/bin/env python
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

import os, sys, gettext, locale, random

import gui, tools

from gui   import window
from tools import consts, log, prefs

BUILD_NAME = os.environ['DECIBEL_BUILD_NAME']
GTK_UI_RES = os.environ['DECIBEL_GTK_UI_RES']
CONFIG_DIR = os.environ['DECIBEL_CONFIG_DIR']
LOCALE_DIR = os.environ['DECIBEL_LOCALE_DIR']

# Init Logger
log = log.Logger()

# Init Random-generator
start_t = tools.timeNow()
random.seed( start_t )

# Init Localization
locale.setlocale(locale.LC_ALL, '')
gettext.textdomain(BUILD_NAME)
gettext.bindtextdomain(BUILD_NAME, LOCALE_DIR)

# Config initialization
appcfg_dir = os.path.join(CONFIG_DIR, BUILD_NAME, '')
user_prefs = prefs.UserPrefs()
if not os.path.exists(appcfg_dir):
    os.mkdir(appcfg_dir)
elif os.path.exists(appcfg_dir + prefs.CONFIG_FILE):
    user_prefs.load(appcfg_dir)

# Merge defaults settings after load user cfg
user_prefs.merge_defaults(prefs.PFX_WINMAIN, [
    ('is-maximized', gui.DEFAULT_MAXIMIZED ),
    ('win-width'   , gui.DEFAULT_WIN_WIDTH ),
    ('win-height'  , gui.DEFAULT_WIN_HEIGHT),
    ('pan-position', gui.DEFAULT_PANED_POS ),
])
# Init gtk ui tree
gui.register_resource(GTK_UI_RES)
# Create the GUI
app_main = window.MainWinApp(consts.APP_PROG_ID, gui.DEFAULT_APP_FLAGS)
# Let's go
log.info('Started')
if app_main.run():
    log.error('Fatal')
if user_prefs.isChanged():
    user_prefs.save(appcfg_dir)
log.info('Stopped')
