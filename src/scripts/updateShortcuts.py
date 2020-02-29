#!/usr/bin/python

TWDIR="../../../texworks/"

from xml.etree import ElementTree
import LaTeX
from LaTeX import *
import os.path

LaTeX.staticTranslations = {'Shortcut': {'fr': 'Raccourci'}}

def load(src):
	res = []

	tree = ElementTree.parse(src)
	for action in tree.findall(".//action"):
		name = None
		key = None
		for prop in action.findall("property"):
			if prop.get("name") == "text":
				name = prop.find("string").text
			if prop.get("name") == "shortcut":
				key = prop.find("string").text
		if name and key:
			res.append((tr(Shortcut(key)), tr(name)))
	return res

def save(out, res):
	res.sort(key = lambda x: x[0])

	with open(out, 'w', encoding = 'utf-8') as f:
		print(formatLaTeXTable(res, 'Pl', [trS('Shortcut'), trS('Action')]), file = f)

loadTranslations(TWDIR)

save('shortcutsTeXDocument.tex', load(os.path.join(TWDIR, 'src', 'TeXDocumentWindow.ui')))
save('shortcutsPDFDocument.tex', load(os.path.join(TWDIR, 'src', 'PDFDocumentWindow.ui')))
