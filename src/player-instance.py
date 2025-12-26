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

from gui.mainWindow import MainWindow
from tools import consts, log, prefs

# Init Logger
log = log.Logger(consts.OUTPUT_LOG)

# Init Random-generator
start_t = tools.timeNow()
random.seed( start_t )

# Init Localization
locale.setlocale(locale.LC_ALL, '')
gettext.textdomain(consts.APP_NAME)
gettext.bindtextdomain(consts.APP_NAME, consts.LOCALE_DIR)

# Config initialization
appcfg_dir = os.path.join(consts.CONFIG_DIR, consts.APP_NAME, '')
user_prefs = prefs.UserPrefs( appcfg_dir )
if not os.path.exists(appcfg_dir):
    os.mkdir(appcfg_dir)
elif os.path.exists(appcfg_dir + prefs.CONFIG_FILE):
    user_prefs.load()

# Create the GUI
win_main = MainWindow(user_prefs)

# Let's go
log.info('Started')
gui.startUp()
log.info('Stopped')
