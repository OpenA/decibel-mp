#!/usr/bin/env sh
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

HOMEURL="@HOMEURL@"
APPNAME="@APPNAME@"
DATADIR="@DATADIR@"
VERSION="@VERSION@"

PYDIR="$DATADIR/$APPNAME"

p_ctrl=''
p_list=''

for i in "$@"; do
  case $i in
    --help | -h)
      echo ""
      echo "Usage: decibel-mp [options] [FILE(s)]"
      echo ""
      exit
      ;;
    --version | -v)
      echo "$APPNAME-$VERSION"
      exit
      ;;
    --remote-prev  | -Z  ) p_ctrl=PREV  ;;
    --remote-next  | -X  ) p_ctrl=NEXT  ;;
    --remote-pause | -P  ) p_ctrl=PAUSE ;;
    --remote-clear | -C  ) p_ctrl=CLEAR ;;
    --remote-shufl | -H  ) p_ctrl=SHUFFLE ;;
    --remote-vol=* | -V=*) p_ctrl=VOLUME; p_list=${i#*=} ;;
    --remote-add=* | -A=*) p_ctrl=ADD   ; p_list=${i#*=} ;;
    --remote-set=* | -S=*) p_ctrl=SET   ; p_list=${i#*=} ;;
  esac
done

if [ ! -z $p_ctrl ]; then
  python3 "$PYDIR/remote-control.py" "$p_ctrl" "$p_list"
else
  python3 "$PYDIR/player-instance.py"
fi
