from xml.etree import ElementTree
import math, os, locale

def makeLaTeXsafe(s):
	if s is None: return ''
	return s.replace("\\", "\\textbackslash ").replace("_", "\\_").replace("{", "\\{").replace("}", "\\}").replace("&", "\\&").replace("#RET#", "{\\AutoCompRet}").replace("#INS#", "{\\AutoCompIns}").replace("#", "\\#").replace("-", "{-}")

class VerbatimLaTeX:
	def __init__(self, s):
		self.str = s

def columnWidths(rows):
	rv = []
	for row in rows:
		if isinstance(row, VerbatimLaTeX): continue
		if len(row) > len(rv): rv += [1] * (len(row) - len(rv))
		for iCol in range(len(row)):
			if len(row[iCol]) > rv[iCol]: rv[iCol] = len(row[iCol])
	return rv

def formatLaTeXTable(data, colSpec, headers = None):
	rows = [[makeLaTeXsafe(col).rstrip() for col in row] if not isinstance(row, VerbatimLaTeX) else row for row in data]
	widths = columnWidths(rows)
	fmt = ''
	for i in range(len(widths)):
		if i > 0: fmt += ' & '
		if i < len(widths) - 1: fmt += '{{{0}:{1}}}'.format(i, widths[i])
		else: fmt += '{{{0}}}'.format(i)
	fmt += r' \\'

	top = [r'\begin{{longtable}}{{{0}}}'.format(colSpec), r'\toprule']
	if headers is not None:
		top += [fmt.format(*headers), r'\midrule \endhead']
	bottom = [r'\bottomrule', r'\end{longtable}']

	return '\n'.join(top + [fmt.format(*row) if not isinstance(row, VerbatimLaTeX) else row.str for row in rows] + bottom)

def columnize(items, numCols = 2):
	n = math.ceil(len(items) / numCols)

	rv = []
	for iRow in range(n):
		rv.append([items[iCol * n + iRow] if iCol * n + iRow < len(items) else None for iCol in range(numCols)])
	return rv

################################################################################
# Translation code
################################################################################

_tsTw = None
_tsQt = None
_lang = 'en'

class Shortcut:
	def __init__(self, keySequence):
		self.keys = [v.replace('+', '\n').replace('\n\n', '\n+').split() for v in keySequence.split(',')]

def loadTranslations(TwDir, lang = None):
	global _tsTw, _tsQt, _lang
	myLocales = {'fr': 'fr_FR'}

	if lang is None:
		# Auto-detect language
		lang = os.path.basename(os.getcwd())

	_lang = lang

	if lang == 'en':
		_tsTw = None
		_tsQt = None
		return


	if lang in myLocales:
		locale.setlocale(locale.LC_ALL, myLocales[lang])
	else:
		print('Warning: Could not determine/set locale for "{0}"'.format(lang))

	try:
		_tsTw = ElementTree.parse(os.path.join(TwDir, 'trans', 'TeXworks_{0}.ts'.format(lang)))
	except FileNotFoundError:
		print('Warning: could not find TeXworks translations for "{0}"'.format(lang))
	try:
		_tsQt = ElementTree.parse(os.path.join(TwDir, 'trans', 'qt', 'qtbase_{0}.ts'.format(lang)))
	except FileNotFoundError:
		print('Warning: could not find Qt translations for "{0}"'.format(lang))

def _translate(s, context, ts, printWarnings = True):
	if ts is None: return s

	if context is not None:
		c = ts.findall('./context[name=\'{0}\']'.format(context))
		if len(c) == 1:
			root = c[0]
		elif len(c) == 0:
			if printWarnings: print('Warning: context "{0}" was not found'.format(context))
			context = None
		else:
			if printWarnings: print('Warning: context "{0}" appears multiple times'.format(context))
			context = None
	if context is None: root = ts

	t = root.findall('.//message[source="{0}"]/translation'.format(s.replace('"', r'\"')))

	if len(t) == 1:
		if t[0].text: return t[0].text
		else: return s
	elif len(t) == 0:
		if printWarnings: print('Warning: no translation found for "{0}"'.format(s))
		return s
	else:
		# Multiple translations were found
		# If they are all the same, use them
		if all([u.text == t[0].text for u in t]):
			if t[0].text: return t[0].text
			return s

		# Otherwise print a warning...
		if printWarnings:
			print('Warning: multiple translations found for "{0}":'.format(s))
			for u in t:
				print('\t' + str(u.text))
		# And use the first that is not empty
		for u in t:
			if u.text: return u.text
		return s

def tr(s, context = None):
	if isinstance(s, Shortcut):
		return ','.join(['+'.join([_translate(k, None, _tsQt, printWarnings = False) for k in seq]) for seq in s.keys])
	return _translate(s, context, _tsTw)

# Static translations
def trS(s):
	if s in staticTranslations and _lang in staticTranslations[s]:
		return staticTranslations[s][_lang]
	return s
