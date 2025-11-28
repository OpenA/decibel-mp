
pydir := ../dist/share/decibel-mp

subdirs = gui tools media media/track media/format modules 

all:
	@echo "nothing to do"

$(subdirs):
	install -m 755 -d $(pydir)/$(@)
	install -m 644 $(@)/*.py $(pydir)/$(@)

install: $(subdirs)
	install -m 755 -d $(pydir)/gtk
	install -m 644 gtk/*.ui $(pydir)/gtk
	install -m 644 ./*.py $(pydir)

.PHONY: all $(subdirs)
