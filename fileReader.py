"""
	fileReader.py

	File Reader Module
	------------------

	This module manages reading the text files outputted from the AS400.  You can 
	read the files, filter lines of text that are not prefferred, and pass the
	appropriate lines of text to the CSVCreator class.

"""

import stringMan as s

class TxtFileReader(object):
	"""
	This object manages opening the incoming text file, creating a TxtBuffer
	object, destroying it and moving on to the next line.  The object also
	manages when the read text is in the header.
	"""
	def __init__(self, filenameIn,*headers):
		"""
	This initializes the TxtFileReader object.  It stops the program if a
	file cannot be opened.
		"""
		self.reading = True
		self.buffer = None
		self.fid = None
		self.headers = headers
		try:
			self.fid = open(filenameIn,'r')
		except IOError:
			print(filenameIn + " does not exist in this directory.")
			raise SystemExit


	def __del__(self):
		"""
	When the object is destroyed, this method will close the file.
		"""
		if self.fid is not None:
			self.fid.close()

	def getNextLine(self):
		"""
	This method creates a new TxtBuffer object.  It tells the program when
	There is no more text to be read.
		"""
		if len(self.headers) != 0:
			self.buffer = TxtBuffer(self.fid,self.headers[0])
		else:
			self.buffer = TxtBuffer(self.fid)
		self._setReading()
		if self._isReturnLine():
			return self.buffer
		else:
			return None

	def _isReturnLine(self):
		"""
	Checks buffer to see if it's unwanted.
		"""
		if self.buffer.returnLine:
			return True
		return False

	def _setReading(self):
		"""
	This method sets the reading method to false if there are no more
	lines of text read from the file.
		"""
		if self.buffer.text == '':
			self.reading = False

class TxtBuffer(object):
	"""
	This class screens the string produced by the readline method
	from the TxtFileReader class.  It checks for the header, the sum
	lines and blank lines.
	"""

	def __init__(self,fid,beginning=True,key=None):
		"""
	This initializes instance variables such as keys, the size of the 
	string and the content read from the TxtFileReader() object
		"""
		self.key = key
		self.text = fid.readline()
		self.size = len(self.text)
		if beginning:
			self.pos = 0
		else:
			self.pos = self.size - len(self.key)
		if key is None:
			self.returnLine = True
		else:
			self.returnLine = self._checkReturnLine()

	def _checkReturnLine(self):
		"""
	This method screens the string output for undesirable strings
		"""
		if self._isSpecialLine(self.key,self.pos):
			return False
		return True

	def _setKey(self,key):
		"""
	Sets key variable
		"""
		self.key = key

	def _setPosition(self,direction):
		"""
	This method sets position based off the direction desired
		"""
		if direction:
			self.pos = 0
		else:
			self.pos = self.size - len(self.key)
			if self.pos < 0:
				self.pos = 0


	def _isSpecialLine(self,key,loc,wc=None):
		"""
	This method is a general method that returns a boolean if the text you're
	looking for is where you expect it to be.
		"""
		if s.wildSearch(self.text,key,wc) == loc :
			return True
		return False

	def getText(self,clip = 0):
		"""
	This method returns the instance text variable.  It's called if the text
	passes all of the tests.  It intentionally removes the last two characters
	to prevent extra new line characters from being passed to the csv.
		"""
		if clip == 0:
			return self.text
		else:
			return self.text[:-clip]

class MapReader(object):
	def __init__(self,fileIn):
		self.delim = '\t'
		self.fid = None
		self.fileName = fileIn
		self.reading = True
		self._openFile()

	def __del__(self):
		if self.fid is not None:
			self.fid.close()

	def _openFile(self):
		try:
			self.fid = open(self.fileName,'r')
		except IOError:
			print('Cannot find ' + self.fileName + ' in directory.')
			raise SystemExit

	def getMap(self):
		mapOut = {}
		while self.reading:
			key,value = self._getNextPair()
			if key is not None:
				mapOut[key] = value
		return mapOut

	def _getNextPair(self):
		text = self.fid.readline()
		if text == '':
			self.reading = False
		else:
			key = s.subStrByChar(text,'','\t')
			key = s.removeSpaces(key)
			value = s.subStrByChar(text,'\t','\n')
			value = s.removeSpaces(value)
			return key,value
		return None,None
