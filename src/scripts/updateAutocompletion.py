#!/usr/bin/python

TWDIR="../../../texworks/"

from LaTeX import *
import os.path

def load(src):
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
	return rules

def toList(rules):
	items = []

	aliases = {}
	for k, v in rules.items():
		if not v in aliases: aliases[v] = []
		if k != v: aliases[v].append(k)

	for a in aliases:
		uniqueAliases = set(s[1:] if s[0] == '\\' else s for s in aliases[a])
		if len(uniqueAliases) == 0: items.append(('', '', a))
		else:
			items += [(ua if ua in aliases[a] else '', '\\' + ua if '\\' + ua in aliases[a] else '', a) for ua in uniqueAliases]
	return items

def save(out, items):
	items.sort(key = lambda x: (x[2].lower(), x[0].lower(), x[1].lower()))

	with open(out, 'w', encoding = 'utf-8') as f:
		print(formatLaTeXTable(items, r'>{\footnotesize}p{15mm}>{\footnotesize}p{15mm}>{\footnotesize}p{95mm}'), file = f)

loadTranslations(TWDIR)

for out, src in (('Basic', 'basic'), ('Beamer', 'beamer'), ('Context', 'context'), ('LatexPkg', 'latex-pkg'), ('Latex', 'latex')):
	save('autocompletion{0}.tex'.format(out), toList(load(os.path.join(TWDIR + 'res', 'resfiles', 'completion', 'tw-{0}.txt'.format(src)))))
