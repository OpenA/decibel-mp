
prefix  ?= /opt/decibel-mp
bindir  ?= bin
datadir ?= share

pkginfo = $(shell cat res/control-install)
appname = $(shell echo '${pkginfo}' | grep -Po 'Package: \K[^ ]+')
version = $(shell echo '${pkginfo}' | grep -Po 'Version: \K[^ ]+')

PREFIX  = $(prefix)
BINDIR  = $(prefix)/$(bindir)
DATADIR = $(prefix)/$(datadir)
MANDIR  = $(DATADIR)/man/man1
APPDIR  = $(DATADIR)/applications
ICONDIR = $(DATADIR)/pixmaps
LCDIR   = $(DATADIR)/locale
PYDIR   = $(DATADIR)/$(appname)

CONF_IN = -e 's!@DATADIR@!$(DATADIR)!'\
          -e 's!@APPNAME@!$(appname)!'\
          -e 's!@VERSION@!$(version)!'

wrkdir = build
resdir = res
locdir = $(wrkdir)/mo

all: locales
	@ sed $(CONF_IN) $(resdir)/decibel-mp.sh > $(wrkdir)/decibel-mp

locales:
	mkdir -p $(locdir)
	$(MAKE) --directory=po

help:
	@echo Usage:
	@echo "make		- not used"
	@echo "make clean	- removes temporary data"
	@echo "make install	- installs data"
	@echo "make uninstall	- uninstalls data"
	@echo "make help	- prints this help"
	@echo

install:
	@echo $(PREFIX)
	$(MAKE) --directory=po  install lcdir="$(LCDIR)"
	$(MAKE) --directory=src install pydir="$(PYDIR)"

	install -m 755 -d $(BINDIR) $(DATADIR) $(APPDIR) \
	                  $(MANDIR) $(ICONDIR) $(PYDIR)

	install -m 755 $(wrkdir)/decibel-mp         $(BINDIR)
	install -m 644 $(resdir)/decibel-mp.1       $(MANDIR)
	install -m 644 $(resdir)/decibel-mp.desktop $(APPDIR)

remove:
	rm -f $(BINDIR)/decibel-mp
	rm -f $(MANDIR)/decibel-mp.1
	rm -f $(APPDIR)/decibel-mp.desktop
	rm -rf $(PYDIR)
	$(RMDIR) --ignore-fail-on-non-empty $(BINDIR) $(MANDIR) $(APPDIR)

clean:
	rm -f $(locdir)/*.mo
	rm -f $(wrkdir)/decibel-mp

.PHONY: all
