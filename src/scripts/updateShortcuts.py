#!/usr/bin/python

TWDIR="../../../texworks/"

from xml.etree import ElementTree

def makeLaTeXsafe(s):
	return s.replace("\\", "\\textbackslash ").replace("_", "\\_").replace("{", "\\{").replace("}", "\\}").replace("&", "\\&").replace("#RET#", "{\\AutoCompRet}").replace("#INS#", "{\\AutoCompIns}").replace("#", "\\#").replace("-", "{-}")


def shortcutsToFile(src, out):
	res = []
	l = 0

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
			if len(makeLaTeXsafe(key)) > l: l = len(makeLaTeXsafe(key))

	res.sort(key = lambda x: x[0])

	fmt = "{0:" + str(l + 1) + r"}& {1} \\"
	
	with open(out, 'w') as f:
		print(r"\begin{longtable}{Pl}", file = f)
		print(r"\toprule", file = f)
		print(fmt.format('Shortcut', 'Action'), file = f)
		print(r"\midrule \endhead", file = f)

		for (key, name) in res:
			print(fmt.format(makeLaTeXsafe(key), makeLaTeXsafe(name)), file = f)

		print(r"\bottomrule", file = f)
		print(r"\end{longtable}", file = f)

shortcutsToFile(TWDIR + "src/TeXDocumentWindow.ui", "shortcutsTeXDocument.tex")
shortcutsToFile(TWDIR + "src/PDFDocumentWindow.ui", "shortcutsPDFDocument.tex")

