MANUAL_LANG=$(notdir $(abspath .))

SYNCTEX = -synctex=1

WINDOWS = $(if $(filter .exe,$(suffix $(SHELL))),"y")
SUPRESSOUT = > $(if $(WINDOWS),nul,/dev/null)
CP = $(if $(WINDOWS),copy,cp)

.PHONY : all pdf html clean dist-clean dist dist-pdf dist-html recursive-clean recursive-dist-clean

all : pdf html

pdf : manual.pdf

html :
	@$(MAKE) -C html

manual.pdf : manual.ind *.tex *.sty images/*.pdf images/*.png
	@lualatex manual
	@bibtex manual
	@lualatex manual
	@lualatex $(SYNCTEX) manual
	
manual.ind : *.tex *.sty
	@lualatex manual
	@makeindex manual

clean :
	rm -f *.aux *.bbl *.log *.out *.idx *.ind *.ilg *.toc

dist-clean : clean
	rm -f manual.pdf *.synctex *.synctex.gz

recursive-clean : clean
	@$(MAKE) -C html clean

recursive-dist-clean : dist-clean
	@$(MAKE) -C html dist-clean

dist : dist-pdf dist-html

dist-pdf : manual.pdf
	@mkdir -p ../../pdf/$(MANUAL_LANG)
	@$(CP) manual.pdf ../../pdf/$(MANUAL_LANG)/TeXworks-manual-$(MANUAL_LANG).pdf

dist-html :
	$(MAKE) -C html dist
