#!/usr/bin/python

"""
	main.py
	-------

	Main Routine for AR Import

"""

import arBuilder as ab
import arReader as ar

#fn = 'AR.txt'
fn = 'AR_new2.txt'
#fn = 'toughCookie.txt'

def main():
	print("Open reader...")
	reader = ar.ARReader(fn)
	print("Creating csv...")
	csv = ab.ARCreator()

	print("Building...")
	while reader.reading:
		newLine = reader.getNextLine()
		if newLine is not None:
			csv.writeToCSV(newLine.getText())

	print("Done!")

def main2():
	reader = ar.ARReader(fn)
	while reader.reading:
		nl,e = reader.getNextLine()
		if nl is not None:
			print(nl.getText())
			print(e)


if __name__ == "__main__":
	main()