#!/usr/bin/python

TWDIR="../../../texworks/"

from LaTeX import *

def autocompletionToFile(src, out):
	with open(src, 'r', encoding = 'utf-8') as f:
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
		items.append((v1, v2, v3))
	
	items.sort(key = lambda x: x[2].lower())

	with open(out, 'w', encoding = 'utf-8') as f:
		print(formatLaTeXTable(items, r'>{\footnotesize}p{15mm}>{\footnotesize}p{15mm}>{\footnotesize}p{95mm}'), file = f)

loadTranslations(TWDIR)

autocompletionToFile(TWDIR + "res/resfiles/completion/tw-basic.txt", "autocompletionBasic.tex")
autocompletionToFile(TWDIR + "res/resfiles/completion/tw-latex.txt", "autocompletionLatex.tex")

