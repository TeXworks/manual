#!/usr/bin/python

TWDIR="../../../texworks/"

from xml.etree import ElementTree
import LaTeX
from LaTeX import *

LaTeX.staticTranslations = {'Shortcut': {'fr': 'Raccourci'}}

def shortcutsToFile(src, out):
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

	res.sort(key = lambda x: x[0])

	with open(out, 'w', encoding = 'utf-8') as f:
		print(formatLaTeXTable(res, 'Pl', [trS('Shortcut'), trS('Action')]), file = f)

loadTranslations(TWDIR)

shortcutsToFile(TWDIR + "src/TeXDocumentWindow.ui", "shortcutsTeXDocument.tex")
shortcutsToFile(TWDIR + "src/PDFDocumentWindow.ui", "shortcutsPDFDocument.tex")

