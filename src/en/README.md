Introduction
================================================================================

This package contains the sources to typeset "A short manual for TeXworks".

TeXworks is an open-source, cross-platform TeX editor designed to lower the
entry barrier to the TeX world. See http://www.tug.org/texworks/ for more
information.




Typesetting
================================================================================

To typeset this document, you need LaTeX. This is usually provided by a TeX
distribution such as:
 * TeXLive (http://www.tug.org/texlive/)
 * MiKTeX (http://www.miktex.org/)
 * MacTeX (http://www.tug.org/mactex/)

Make sure you have the following required LaTeX packages installed:
	amsmath, amssymb, array, babel, babel-french, booktabs, calc, color, ec,
	etoolbox, fancyhdr, fancyvrb, fncychap, fontenc, footmisc, framed, graphicx,
	hyperref, idxlayout, inputenc, keystroke, lmodern, longtable, makeidx,
	metalogo, microtype, needspace, sectsty, tocbibind, upquote, url, wrapfig,
and the ZapfChancery font.

When using TeXLive, these can be installed by running
```
	tlmgr install amsfonts amsmath babel babel-french booktabs ec etoolbox \
	              fancyhdr fancyvrb fncychap footmisc framed graphics hyperref \
	              idxlayout keystroke latex lm metalogo microtype needspace \
	              sectsty tocbibind tools upquote url wrapfig zapfchan
```
from the command line.

If you intend to typeset in the HTML format, you also need tex4ht.




Disclaimer
================================================================================

Copyright (C) 2010-2024  Alain Delmotte, Stefan Löffler, and contributors.
Some rights reserved.

Unless noted otherwise, the icons in the images/ folder are taken from the
TeXworks project, the Tango project, or were made for this work.

This manual is free documentation: you can redistribute it and/or modify it
under the terms of either:

  * the CC-BY-SA license as published by Creative Commons; either version 3 of
    the License, or (at your option) any later version.

or

  * the GNU General Public License as published by the Free Software Foundation;
    either version 2 of the License, or (at your option) any later version.

or both in parallel. For details, see the files COPYING.CC-by-sa-3.0
and COPYING.GPLv2.
