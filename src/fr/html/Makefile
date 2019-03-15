MANUAL_LANG=$(notdir $(abspath ..))

Logos = images/Linux.png images/Mac.png images/Windows.png images/TeXworks.png images/example.png
EpsFromPdf = images/MacCmdKey.eps images/MacOptKey.eps images/LMB.eps images/RMB.eps
EpsFromPng = images/toolbar1.eps images/toolbar2.eps images/iconTypeset.eps images/iconAbortTypesetting.eps images/TeXworks.eps images/Linux.eps images/Mac.eps images/Windows.eps images/interface-Tw.eps images/consoleOutput.eps images/errorParsingScript.eps 
EpsFromJpg = images/rechremp.eps

IMAGES = $(Logos) $(EpsFromPdf) $(EpsFromPng) ${EpsFromJpg}

HTOPTS = "manual,info,2,imgdir:images/,sec-filename,next,index=2,url-enc" "" "-S*"

# Ghostscript 9.14/9.15 dropped the 'epswrite' output device in favor of the new
# 'eps2write' output device. Prefer the latter, but fallback to the former for
# older Ghostscript versions.
GS_DEVICE = $(shell LANG=C; gs -h | grep -o eps2write || echo epswrite)

WINDOWS = $(if $(filter .exe,$(suffix $(SHELL))),"y")
SUPRESSOUT = > $(if $(WINDOWS),nul,/dev/null)
CP = $(if $(WINDOWS),copy,cp)

.PHONY : html clean dist-clean dist dist-pdf dist-html

SOURCES = index.tex $(filter-out manuel.tex,$(subst ../,,$(wildcard ../*.tex ../*.sty)))

html : index.html

index.html : $(IMAGES) $(SOURCES) index.ind manual.cfg tex4ht.env
	@htlatex index $(HTOPTS)
	@htlatex index $(HTOPTS)

%.tex : ../%.tex
	$(CP) $< $@
%.sty : ../%.sty
	$(CP) $< $@
index.tex : ../manuel.tex
	$(CP) $< $@

images/Linux.png : ../images/Linux.pdf
	@mkdir -p images
	@gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pngalpha -sstdout=%stderr -sOutputFile=- "$<" 2$(SUPRESSOUT) | convert png:- -resize 48x48 $@ $(SUPRESSOUT)
images/Mac.png : ../images/Mac.pdf
	@mkdir -p images
	@gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pngalpha -sstdout=%stderr -sOutputFile=- "$<" 2$(SUPRESSOUT) | convert png:- -resize 48x48 $@ $(SUPRESSOUT)
images/Windows.png : ../images/Windows.pdf
	@mkdir -p images
	@gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pngalpha -sstdout=%stderr -sOutputFile=- "$<" 2$(SUPRESSOUT) | convert png:- -resize 48x48 $@ $(SUPRESSOUT)
images/TeXworks.png : ../images/TeXworks.png
	@mkdir -p images
	@convert ../images/TeXworks.png -resize 100x100 images/TeXworks.png $(SUPRESSOUT)
images/example.png : ../images/example.pdf
	@mkdir -p images
	@gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pngalpha -sstdout=%stderr -sOutputFile=- "$<" 2$(SUPRESSOUT) | convert png:- -resize 48x48 $@ $(SUPRESSOUT)
images/%.eps : ../images/%.pdf
	@echo "Creating image $@ (from $<)"
	@mkdir -p images
	@gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=$(GS_DEVICE) -sOutputFile="$@" "$<" $(SUPRESSOUT)
images/%.eps : ../images/%.png
	@echo "Creating image $@ (from $<)"
	@mkdir -p images
	# Some versions of convert refuse to produce .eps files due to security concerns
	@convert "$<" "$@" $(SUPRESSOUT) 2$(SUPRESSOUT) || convert "$<" ppm: | pnmtops -noturn | eps2eps - "$@"
images/%.eps : ../images/%.jpg
	@echo "Creating image $@ (from $<)"
	@mkdir -p images
	# Some versions of convert refuse to produce .eps files due to security concerns
	@convert "$<" "$@" $(SUPRESSOUT) 2$(SUPRESSOUT) || convert "$<" ppm: | pnmtops -noturn | eps2eps - "$@"


index.ind : images $(SOURCES) manual.cfg tex4ht.env
	@echo "Creating index..."
	@echo "   running htlatex..."
	@htlatex index $(HTOPTS)
	@echo "   creating input file..."
	@tex '\def\filename{{index}{idx}{4dx}{ind}} \input  idxmake.4ht'
	@echo "   running makeindex..."
	@makeindex -o index.ind index.4dx

clean : 
	rm -f *.tex *.sty idxmake.* *.aux *.log
	rm -f index.4ct index.4tc index.dvi index.idv index.idx index.lg index.log index.out index.tmp index.xref index.4dx index.4ix index.ilg index.ind

dist-clean : clean
	rm -f *.html index.css
	rm -rf images/

dist : dist-html

dist-html : index.html tidy.cfg manual.css
	@mkdir -p ../../../html/TeXworks-manual/$(MANUAL_LANG)/images
	@$(CP) images/*.png ../../../html/TeXworks-manual/$(MANUAL_LANG)/images
	@$(CP) *.html *.css tw-help-title.txt ../../../html/TeXworks-manual/$(MANUAL_LANG)/
	@tidy -config tidy.cfg ../../../html/TeXworks-manual/$(MANUAL_LANG)/*.html || true

