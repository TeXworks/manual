LANGS = $(patsubst %/,manual-%,$(filter-out scripts/,$(wildcard */)))
DISTLANGS = $(patsubst manual-%,dist-%,$(LANGS))
CLEANLANGS = $(patsubst manual-%,clean-%,$(LANGS))
DISTCLEANLANGS = $(patsubst manual-%,dist-clean-%,$(LANGS))

# Be rather specific with '--git-dir' as we do not want to pick up an unrelated
# outer Git repository in case the TeXworks manual sources come from an archive.
GIT_COMMIT = $(shell LANG=C; git --git-dir=../.git rev-parse --short HEAD || echo "")
GIT_DATE_ISO = $(shell LANG=C; git --git-dir=../.git show -s --pretty=%ci HEAD || echo "")
GIT_DATE = $(subst -,,$(word 1,$(GIT_DATE_ISO)))$(subst :,,$(word 2,$(GIT_DATE_ISO)))

# If calling git did not succeed (for whatever reason), try to fetch the info
# from git_version.txt (which is populated during 'git archive')
ifeq ($(GIT_COMMIT),)
	GIT_VERSION_INFO := $(shell cat git_version.txt)
	GIT_COMMIT = $(word 1,$(GIT_VERSION_INFO))
	GIT_DATE = $(subst -,,$(word 2,$(GIT_VERSION_INFO)))$(subst :,,$(word 3,$(GIT_VERSION_INFO)))

	# If we still couldn't figure out the version, stop with an error message
	ifeq ($(findstring %h,$(GIT_COMMIT)),%h)
        $(error "Could not determine the version information. Make sure you use git or a properly exported archive")
	endif
endif


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

