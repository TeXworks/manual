#!/usr/bin/python

TWDIR="../../../texworks/"

from xml.etree import ElementTree
from LaTeX import *
import os.path

acts = set()

def load(src):
	tree = ElementTree.parse(src)

	# parse all menus
	menus = {}
	for menu in tree.findall('.//widget[@class="QMenu"]'):
		name = menu.get("name")
		menus[name] = {'title': menu.find('property[@name="title"]/string').text, 'actions': []}
		for act in menu.findall("addaction"):
			if act.get("name") and act.get("name") != "separator":
				menus[name]['actions'].append(act.get("name"))
	
	# consolidate menus (add actions of submenus to parent menus)
	finished = False
	while not finished:
		# Loop until no more changes are made
		finished = True
		for name in list(menus.keys()):
			# if the menu was removed (i.e., merged into another menu) already,
			# continue
			if not name in menus: continue
			i = 0
			while i < len(menus[name]['actions']):
				a = menus[name]['actions'][i]
				if a in menus:
					# If the action corresponds to a submenu, replace it by the
					# contents of said submenu
					menus[name]['actions'][i:i+1] = menus[a]['actions']
					del menus[a]
					finished = False
				else:
					i += 1
	# return a dict of menus and a list of all actions
	return menus, [a.get('name') for a in tree.findall('.//action') if a.get('name')]

def save(out, menus):
	labels = [(k, m['title']) for k, m in menus.items()]
	labels.sort(key = lambda x: locale.strxfrm(tr(x[1])))

	i = 0
	items = []
	for (key, label) in labels:
		if not key in menus: continue
		if i > 0: items.append(VerbatimLaTeX("%\n\\midrule\n%"))
		items.append(VerbatimLaTeX(r"\multicolumn{{2}}{{c}}{{{label}}} \\".format(label = makeLaTeXsafe(tr(label)))))
		items += columnize(sorted(menus[key]['actions']))
		i += 1

		with open(out, 'w', encoding='utf-8') as f:
			print(formatLaTeXTable(items, 'QQ'), file = f)

loadTranslations(TWDIR)

menus, a = load(os.path.join(TWDIR, 'src', 'TeXDocumentWindow.ui'))
acts |= set(a)
save('menuactionsTeXDocument.tex', menus)

menus, a = load(os.path.join(TWDIR, 'src', 'PDFDocumentWindow.ui'))
acts |= set(a)
save('menuactionsPDFDocument.tex', menus)

_, a = load(os.path.join(TWDIR, 'src', 'CompletingEdit.ui'))
acts |= set(a)

# make unique & sort
acts = list(sorted(acts))

with open("actionsAlphabetical.tex", 'w', encoding = 'utf-8') as f:
	print(formatLaTeXTable(columnize(acts), 'QQ'), file = f)
