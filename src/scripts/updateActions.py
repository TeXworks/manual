#!/usr/bin/python

TWDIR="../../../texworks/"

from xml.etree import ElementTree
from LaTeX import *

acts = []

def getActions(src, out):
	tree = ElementTree.parse(src)
	for action in tree.findall(".//action"):
		if action.get("name"): acts.append(action.get("name"))
	
	menus = {}
	labels = {}
	# parse all menus
	for menu in tree.findall(".//widget"):
		if menu.get("class") != "QMenu": continue
		name = menu.get("name")
		menus[name] = []
		for prop in menu.findall("property"):
			if prop.get("name") == "title": labels[name] = prop.find("string").text
		for act in menu.findall("addaction"):
			if act.get("name") and act.get("name") != "separator":
				menus[name].append(act.get("name"))
	
	# consolidate menus (add actions of submenus to parent menus)
	finished = False
	while not finished:
		finished = True
		for name in list(menus.keys()):
			if name in menus:
				i = 0
				while i < len(menus[name]):
#					print name + " " + str(i) + " " + str(len(menus[name]))
					a = menus[name][i]
					if a in menus:
						del menus[name][i]
						menus[name][i:0] = menus[a]
						del menus[a]
						finished = False
					else:
						i += 1
	
	labels = list(labels.items())
	labels.sort(key = lambda x: locale.strxfrm(tr(x[1])))

	if out is not None:
		i = 0
		items = []
		for (key, label) in labels:
			if not key in menus: continue
			if i > 0: items.append(VerbatimLaTeX("%\n\\midrule\n%"))
			items.append(VerbatimLaTeX(r"\multicolumn{{2}}{{c}}{{{label}}} \\".format(label = makeLaTeXsafe(tr(label)))))
			items += columnize(sorted(menus[key]))
			i += 1

		with open(out, 'w', encoding='utf-8') as f:
			print(formatLaTeXTable(items, 'QQ'), file = f)

#	for menu in tree.findall("/widget/widget/widget"):
#		if menu.get("class") != "QMenu": continue
#		print menu.get("name")
#		for act in menu.findall("addaction"):
#			print "\t" + act.get("name")

#		break

loadTranslations(TWDIR)

getActions(TWDIR + "src/TeXDocumentWindow.ui", "menuactionsTeXDocument.tex")
getActions(TWDIR + "src/PDFDocumentWindow.ui", "menuactionsPDFDocument.tex")
getActions(TWDIR + "src/CompletingEdit.ui", None)


# make unique & sort
acts = list(set(acts))
acts.sort()

with open("actionsAlphabetical.tex", 'w', encoding = 'utf-8') as f:
	print(formatLaTeXTable(columnize(acts), 'QQ'), file = f)
