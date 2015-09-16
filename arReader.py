"""
	arReader.py

	Accounts Receivable Reader Module
	----------------------------------

	This module manages reading of the AR text file.

"""

import fileReader as f
import stringMan as s

#	Diagnostics, True is on, False is off
DIAG = False

#	Search keys
HEAD_KEY 	= 'AMR803\n'
INV_KEY 	= ' '*2 + '_'*6
TRAN_KEY 	= '*' + ' '*8 + '***'
INV_TERM	= '_'*33 + '*'
PT_KEY		= '-------\n'
CUST_KEY 	= '8'
CUST_TERM	= 'TOTAL'


class ARReader(f.TxtFileReader):
	"""
	Extends the TxtFileReader class.  Needs to manage the different
	trash keys and needs to pass the right lines to the builder
	"""
	def __init__(self,filenameIn,rptHdr = True):
		"""
	Initializes ARReader class
		"""
		f.TxtFileReader.__init__(self,filenameIn)
		self.reportHeader = rptHdr
		self.eventState = -1
		self.lock = 0
		self.key = {CUST_KEY:True,INV_KEY:True,TRAN_KEY:True,INV_TERM:True,\
			PT_KEY:False,CUST_TERM:True}

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
		key = self._getKeyDict()

		#	Set the buffer
		self.buffer = ARBuffer(self.fid,key,self.eventState)
		self._setReading()

		#	Auto return null if locked
		if self.lock > 0:
			self.lock -= 1
			#print('Return Lock: ' + str(self.eventState) + '\n' + \
			#	'Lock: ' + str(self.lock))
			return None,None		

		#	Return null if line is header.  Set lock.
		elif self._isHeader():
			self.eventState = -1
			if self.reportHeader:
				self.lock = 6
				self.reportHeader = False
			else:
				self.lock = 3
			self._printDiagnostics(DIAG,False)
			self._setEventState()
			#print('Return Header: ' + str(self.eventState))
			return None,None

		#	Return null if blank.
		elif self._isBlank():
			self._printDiagnostics(DIAG,False)
			#print('Return Blank: ' + str(self.eventState))
			return None,None			

		#	Return buffer and event state
		elif self._isReturnLine():
			self._setEventState()
			self._printDiagnostics(DIAG,True)
			#print('Return Key: ' + str(self.eventState))
			return self.buffer,self.eventState

		else:
			self._setEventState()
			return None,None



	def _getKeyDict(self):
		"""
	Checks the event state and passes a key to the buffer
		"""
		if self.eventState == -1:
			key = CUST_KEY
		elif self.eventState == 0:
			key = INV_KEY
		elif self.eventState == 1 or self.eventState == 2:
			key = TRAN_KEY
		elif self.eventState == 3:
			key = CUST_TERM
		pos = self.key[key]
		keyDict = {key:pos}
		return keyDict
	

	def _isHeader(self):
		"""
	Reads the buffer's header variable and returns boolean
		"""
		if self.buffer.header:
			return True
		return False

	def _isBlank(self):
		"""
	Reads the buffer's blank variable and returns boolean
		"""
		if self.buffer.blank:
			return True
		return False

	def _printDiagnostics(self,onBool,*typeBool):
		"""
	Easily print diagnostic info
		"""
		if onBool:
			if typeBool[0]:
				print(self.buffer)
				print("Text: " + self.buffer.getText(1))
			else:
				print("None")

			print("State: " + str(self.eventState))
			print("Lock: " + str(self.lock))
			print("")
		else:
			if typeBool[0]:
				#print(self.buffer.getText(1))
				pass

	def _setEventState(self):
		"""
	Sets event state of reader to that of buffer
		"""
		self.eventState = self.buffer.eventState


class ARBuffer(f.TxtBuffer):
	"""
	Exteds the TxtBuffer class.
	"""
	def __init__(self, fid, keyIn, es):
		"""
	Inputs: open file, ordered key, and header key that appears randomly
		"""
		f.TxtBuffer.__init__(self,fid)
		self.keyDict = keyIn
		self.headKey = {HEAD_KEY : False}
		self.blankKey = {'\n':True}
		self.eventState = es
		self.header = False
		self.blank = False
		self.returnLine = self._checkNecessaryReturnLine()

	def _checkNecessaryReturnLine(self):
		"""
	Manages the return line functions.  Reads the ivar key and determines
	which function to call.
		"""
		if self._isHeader():
			self.header = True
			#self.eventState = -1
			return False
		if self._isBlank():
			self.blank = True
			return False

		if self.eventState == -1:
			if self._isFlagged(self.keyDict):
				self.eventState += 1
				return True

		elif self.eventState == 0:
			if self._isFlagged({PT_KEY:False}):
				self.eventState = 3
				return False
			elif self._isFlagged(self.keyDict,'_'):
				self.eventState += 1
				return True

		elif self.eventState == 1:
			if self._isFlagged(self.keyDict,'*'):
				self.eventState = 2
				return True

		elif self.eventState == 2:
			if self._isFlagged({INV_TERM:True},'_'):
				self.eventState = 0
				return False
			elif self._isFlagged(self.keyDict,'*'):
				self.eventState = 2
				return True

		elif self.eventState == 3:
			if self._isFlagged(self.keyDict):
				self.eventState = -1
				return True

		else:
			return False


	def _isHeader(self):
		"""
	Checks the header key for a header line
		"""
		if self._isFlagged(self.headKey):
			return True
		return False

	def _isBlank(self):
		"""
	Checks the text for an immediate new line
		"""
		if self._isFlagged(self.blankKey):
			return True
		return False

	def _isFlagged(self,keyIn,wc=None):
		"""
	General function used to manage return line
		"""
		key,pos = keyIn.items()[0]
		self._setKey(key)
		self._setPosition(pos)
		if self._checkReturnLine(wc):
			return False
		return True

	def _isSpecialLine(self,key,loc,wc=None):
		"""
	This uses the new wildSearch technique.
		"""
		if s.newWildSearch(self.text,key,wc) == loc :
			return True
		return False