from xml.etree import ElementTree
import math

def makeLaTeXsafe(s):
	if s is None: return ''
	return s.replace("\\", "\\textbackslash ").replace("_", "\\_").replace("{", "\\{").replace("}", "\\}").replace("&", "\\&").replace("#RET#", "{\\AutoCompRet}").replace("#INS#", "{\\AutoCompIns}").replace("#", "\\#").replace("-", "{-}").replace("'", r"\textquotesingle")

class VerbatimLaTeX:
	def __init__(self, s):
		self.str = s

def columnWidths(rows):
	rv = []
	for row in rows:
		if isinstance(row, VerbatimLaTeX): continue
		if len(row) > len(rv): rv += [0] * (len(row) - len(rv))
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
