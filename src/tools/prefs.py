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

import configparser

CONFIG_FILE = 'settings.ini'
PFX_WINMAIN = 'MainWindow'
PFX_USER    = 'UserPrefs'

class UserPrefs():

    def __init__(self, cfg_dir: str):
        self._cfg = configparser.ConfigParser()
        self._dir = cfg_dir

    def load(self, file: str = CONFIG_FILE):
        """ Load user preferences from the config dir use Ini format """
        with open(self._dir + file, 'r') as input:
            self._cfg.read_file(input)

    def save(self, file: str = CONFIG_FILE):
        """ Save user preferences to the config dir use Ini format """
        with open(self._dir + file, 'w') as output:
            self._cfg.write(output)

    def set(self, key: str, val: str | int | float | bool, pfx: str = PFX_WINMAIN):
        """ Change the value of a preference """
        self._cfg[pfx][key] = f'{val}' if type(val) is not bool else 'yes' if val else 'no'

    def get(self, key: str, pfx: str = PFX_WINMAIN):
        """ Retrieve the value of a preference """
        return self._cfg[pfx][key]

    def set_defaults(self, pfx: str, params: list[tuple]):
        """ Init default values without rewriting existings """
        if pfx not in self._cfg:
            self._cfg.add_section(pfx)
        for (k,v) in params:
            if k not in self._cfg[pfx]:
                self.set(k, v, pfx)

    def get_int  (self, key: str, pfx: str = PFX_WINMAIN): return int      (self.get(key, pfx))
    def get_bool (self, key: str, pfx: str = PFX_WINMAIN): return ('yes' == self.get(key, pfx))
    def get_float(self, key: str, pfx: str = PFX_WINMAIN): return float    (self.get(key, pfx))
