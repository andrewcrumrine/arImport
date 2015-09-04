"""
	This module manages the files and logs the output to the user.
"""

import os

class FileList():
	def __init__(self,path=''):
		self.path = path
		self.files = self.__generateList()

	def __generateList(self):
		os.chdir(self.path)
		txtFiles = []
		files = os.listdir(os.curdir)
		for f in files:
			if self.__isTxtFile(f):
				txtFiles.append(self.path + '/' + f)
		os.chdir('..')
		return txtFiles

	def __isTxtFile(self,f_str):
		if f_str[-4:] == '.txt':
			return True
		return False

	def getNextFile(self,descending=True):
		if descending:
			return self.files.pop()
		else:
			fileOut = self.files[0]
			self.files.remove(self.files[0])
			return fileOut
	def isEmpty(self):
		if len(self.files) == 0:
			return True
		return False