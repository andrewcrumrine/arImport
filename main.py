#!/usr/bin/python

"""
	main.py
	-------

	Main Routine for AR Import

"""

import arBuilder as ab
import arReader as ar

#fn = 'AR.txt'
fn = 'toughCookie.txt'

reader = ar.ARReader(fn)

while reader.reading:
	newLine = reader.getNextLine()
