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

import os, sys

class Logger:

    def __init__(self, logfile: str = None):
        """ Constructor """
        self._log_output_fd = None
        self._bak_stderr_fd = None
        # ~
        if (logfile != None and len(logfile) != 0):
            self._log_output_fd = open(logfile, 'a')
            self._bak_stderr_fd = os.dup(sys.stderr.fileno())
            os.dup2(self._log_output_fd.fileno(), sys.stderr.fileno())

    def __del__(self):
        """ Destructor """
        if (self._log_output_fd != None):
            os.dup2 (self._bak_stderr_fd, sys.stderr.fileno())
            os.close(self._bak_stderr_fd)
            self._log_output_fd.close()
        # ~
        self._log_output_fd = None
        self._bak_stderr_fd = None

    @staticmethod
    def puts(_T: str, msg: str):
        """ Custom message  """
        sys.stderr.write('%-6s %s\n' % (_T, msg))
        sys.stderr.flush()

    @staticmethod
    def info(inf: str):
        """ Information message """
        sys.stderr.write('INFO: {inf}\n')
        sys.stderr.flush()

    @staticmethod
    def error(err: str):
        """ Error message """
        sys.stderr.write('ERROR: {err}\n')
        sys.stderr.flush()
