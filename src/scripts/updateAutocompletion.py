#!/usr/bin/python

TWDIR="../../../texworks/"

from xml.etree import ElementTree


def makeLaTeXsafe(s):
	return s.replace("\\", "\\textbackslash ").replace("_", "\\_").replace("{", "\\{").replace("}", "\\}").replace("&", "\\&").replace("#RET#", "{\\AutoCompRet}").replace("#INS#", "{\\AutoCompIns}").replace("#", "\\#").replace("-", "{-}")

def autocompletionToFile(src, out):
	with open(src, 'r') as f:
		rules = {}
		for line in f:
			if line[0] == '%': continue
			line = line.strip().split(':=')
			if len(line) == 2:
				(key, value) = line
			else:
				key = value = line[0]
			rules[key] = value
	
	items = []
	n1 = n2 = 0
	for key in list(rules.keys()):
		if not key in rules: continue
		v1 = v2 = ''
		v3 = rules[key]
		if key == v3:
			pass
		elif key[0] == '\\':
			v2 = key
			if key[1:] in rules and rules[key[1:]] == v3:
				v1 = key[1:]
				del rules[key[1:]]
		else:
			v1 = key
			if "\\" + key in rules and rules["\\" + key] == v3:
				v2 = "\\" + key
				del rules["\\" + key]
		del rules[key]
		if len(makeLaTeXsafe(v1)) > n1: n1 = len(makeLaTeXsafe(v1))
		if len(makeLaTeXsafe(v2)) > n2: n2 = len(makeLaTeXsafe(v2))
		items.append((v1, v2, v3))
	
	items.sort(key = lambda x: x[2].lower())
	fmt = "{0:" + str(n1) + "} & {1:" + str(n2) + r"} & {2} \\"

	with open(out, 'w') as f:
		print(r"\begin{longtable}{>{\footnotesize}p{15mm}>{\footnotesize}p{15mm}>{\footnotesize}p{95mm}}", file = f)
		print(r"\toprule", file = f)

		for (v1, v2, v3) in items:
			print(fmt.format(makeLaTeXsafe(v1), makeLaTeXsafe(v2), makeLaTeXsafe(v3)), file = f)

		print(r"\bottomrule", file = f)
		print(r"\end{longtable}", file = f)


autocompletionToFile(TWDIR + "res/resfiles/completion/tw-basic.txt", "autocompletionBasic.tex")
autocompletionToFile(TWDIR + "res/resfiles/completion/tw-latex.txt", "autocompletionLatex.tex")

