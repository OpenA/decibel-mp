
modir   := ../build/mo
lcdir   := ../dist/share/locale
appname := decibel-mp

locales = $(wildcard *.po)
objects = $(patsubst %.po,%.mo,$(locales))
msgdirs = $(patsubst %.po,%/LC_MESSAGES,$(locales))

all: $(objects)

%.mo: %.po
	@ if test -f $(modir)/$(@);\
			then echo "Update \033[1m$(@)\033[0m locale";\
			else echo "Create \033[1m$(@)\033[0m locale";\
		fi
	@ msgfmt --output-file="$(modir)/$(@)" "$(<)"

%/LC_MESSAGES: $(modir)/%.mo
	install -m 755 -d $(lcdir)/$(@)
	install -m 644 "$(<)" $(lcdir)/$(@)/$(appname).mo

install: $(msgdirs)

.PHONY: all
