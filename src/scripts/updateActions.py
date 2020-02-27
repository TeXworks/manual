#!/usr/bin/python

TWDIR="../../../texworks/"

from xml.etree import ElementTree

def makeLaTeXsafe(s):
	return s.replace("_", r"\_")

def format2Columns(items):
	ret = ""
	n = len(items)
	if n % 2 == 1: n += 1
	
	l = 0
	for i in range(int(n / 2)):
		if len(makeLaTeXsafe(items[i])) > l: l = len(makeLaTeXsafe(items[i]))
	
	fmt = "{0:" + str(l + 1) + "}& "
	for i in range(int(n / 2)):
		ret += fmt.format(makeLaTeXsafe(items[i]))
		if i + n / 2 < len(items):
			ret += makeLaTeXsafe(items[i + int(n / 2)]) + " "
		ret += "\\\\\n"
	return ret.strip()


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
	labels.sort(key = lambda x: x[1])
	if out is not None:
		with open(out, 'w') as f:
			print(r'\begin{longtable}{QQ}', file = f)
			print(r'\toprule', file = f)

			i = 0
			for (key, label) in labels:
				if not key in menus: continue
				if i > 0: print("%\n\\midrule\n%", file = f)
				print(r"\multicolumn{{2}}{{c}}{{{label}}} \\".format(label = makeLaTeXsafe(label)), file = f)
				items = menus[key]
				items.sort()
				print(format2Columns(items), file = f)
				i += 1

			print(r"\bottomrule", file = f)
			print(r"\end{longtable}", file = f)
		
#	for menu in tree.findall("/widget/widget/widget"):
#		if menu.get("class") != "QMenu": continue
#		print menu.get("name")
#		for act in menu.findall("addaction"):
#			print "\t" + act.get("name")

#		break

getActions(TWDIR + "src/TeXDocumentWindow.ui", "menuactionsTeXDocument.tex")
getActions(TWDIR + "src/PDFDocumentWindow.ui", "menuactionsPDFDocument.tex")
getActions(TWDIR + "src/CompletingEdit.ui", None)


# make unique & sort
acts = list(set(acts))
acts.sort()

with open("actionsAlphabetical.tex", 'w') as f:
	print(r"\begin{longtable}{QQ}", file = f)
	print(r"\toprule", file = f)
	print(format2Columns(acts), file = f)
	print(r"\bottomrule", file = f)
	print(r"\end{longtable}", file = f)
