LANGS = $(patsubst %/,manual-%,$(wildcard */))
DISTLANGS = $(patsubst manual-%,dist-%,$(LANGS))
CLEANLANGS = $(patsubst manual-%,clean-%,$(LANGS))
DISTCLEANLANGS = $(patsubst manual-%,dist-clean-%,$(LANGS))

# Be rather specific with '--git-dir' as we do not want to pick up an unrelated
# outer Git repository in case the TeXworks manual sources come from an archive.
GIT_COMMIT = $(shell LANG=C; git --git-dir=../.git rev-parse --short HEAD)
GIT_DATE = $(subst -,,$(word 1, $(shell LANG=C; git --git-dir=../.git show -s --pretty=%ci HEAD)))

.PHONY : all clean dist dist-clean $(LANGS) $(DISTLANGS) $(CLEANLANGS) $(DISTCLEANLANGS)

all : $(LANGS)

clean : $(CLEANLANGS)

dist : $(DISTLANGS)
	cd ../html && zip -r TeXworks-manual-html-$(GIT_DATE)-$(GIT_COMMIT).zip TeXworks-manual

dist-clean : $(DISTCLEANLANGS)

$(LANGS) : 
	@$(MAKE) -C $(patsubst manual-%,%,$@)

$(DISTLANGS) :
	@$(MAKE) -C $(patsubst dist-%,%,$@) dist

$(CLEANLANGS) :
	@$(MAKE) -C $(patsubst clean-%,%,$@) recursive-clean

$(DISTCLEANLANGS) :
	@$(MAKE) -C $(patsubst dist-clean-%,%,$@) recursive-dist-clean

