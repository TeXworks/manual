#!/usr/bin/python

TWDIR="../../../texworks/"

from xml.etree import ElementTree
from LaTeX import *

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
			res.append((key, name))

	res.sort(key = lambda x: x[0])

	with open(out, 'w') as f:
		print(formatLaTeXTable(res, 'Pl', ['Shortcut', 'Action']), file = f)

shortcutsToFile(TWDIR + "src/TeXDocumentWindow.ui", "shortcutsTeXDocument.tex")
shortcutsToFile(TWDIR + "src/PDFDocumentWindow.ui", "shortcutsPDFDocument.tex")

