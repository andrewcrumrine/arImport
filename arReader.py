"""
	arReader.py

	Accounts Receivable Reader Module
	----------------------------------

	This module manages reading of the AR text file.

"""

import fileReader as f

HEAD_KEY = 'AMR803 '
CUST_KEY = '8'
DASH_KEY = '-------'


class ARReader(f.TxtFileReader):
	"""
	Extends the TxtFileReader class.  Needs to manage the different
	trash keys and needs to pass the right lines to the builder
	"""
	def __init__(self,filenameIn):
		"""
	Initializes ARReader class
		"""
		f.TxtFileReader.__init__(self,filenameIn)
		self.eventState = 0
		self.lock = False
		self.key = {'\n':True, CUST_KEY:True,DASH_KEY:True}

	def __del__(self):
		"""
	Closes open file if it exists
		"""
		f.TxtFileReader.__del__(self)

	def getNextLine(self):
		"""
	This method creates a ARBuffer object. It tells the program when the
	file is empty.
		"""
		self.buffer = ARBuffer(self.fid,key)
		self._setReading()
		if self._isReturnLine():
			return self.buffer
		elif self._isHeader():
			self.eventState = 0
			self.lock = True
			return None
		elif self._unlock():
			self.lock = False
			self.eventState += 1
			return self.buffer
		else:
			self.eventState -= 1
			return None

	def _setKey(self):
		"""
	Checks the event state and passes a key to the buffer
		"""
		if eventState == 0:
			key = CUST_KEY
		elif eventState == 1:
			key = DASH_KEY
	
	def _unlock(self):
		"""
	Reads the """

class ARBuffer(f.TxtBuffer):
	"""
	Exteds the TxtBuffer class.
	"""
	def __init__(self, fid, keyIn):
		"""
	Inputs: open file, ordered key, and header key that appears randomly
		"""
		f.TxtBuffer.__init__(self,fid)
		self.key = keyIn
		self.headKey = {HEAD_KEY : False}
		self.header = False
		self.returnLine = self._checkNecessaryReturnLine()

	def _checkNecessaryReturnLine(self):
		"""
	Manages the return line functions.  Reads the ivar key and determines
	which function to call.
		"""
		if self._isHeader():
			self.header = True
			return False
		key,pos = self.key.items()[0]
		if key == '\n':
			return False
		elif key == CUST_KEY:
			self._setKey(key)
			self._setPosition(pos)
			if not self._checkReturnLine():
				return False
		elif key == DASH_KEY:
			self._setKey(key)
			self._setPosition(pos)
			if not self._checkReturnLine():
				return False
		return True

	def _isHeader(self):
		"""
	Checks the header key for a header line
		"""
		key,pos = self.headKey.items()[0]
		self._setKey(key)
		self._setPosition(pos)
		return self._checkReturnLine()