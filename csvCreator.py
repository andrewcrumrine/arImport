"""
	csvCreator.py

	CSV Creator Module
	----------------------

	This module contains a general CSV writer read from the 
	file reader module.  It anticipates a line of text generated
	by a report and converts the text into a csv.

"""

class CSVCreator(object):
	"""
	CSVCreator on the Comment Builder Module builds a csv with every comment
	fields inputed from the AS400
	"""

	def __init__(self,filenameIn=None):
		"""
	This initializes the CSVCreator object.
		"""
		self.fileIn = filenameIn
		self.fileOut = 'out.csv'
		self.text = ''
		self.fid = None
		self.csvCreated = False

		self.header = []
		self.indices = {}

		if type(self) == CSVCreator:
			self._createCSV()

	def __del__(self):
		"""
	This method runs when the object is destroyed.  It closes the file.
		"""
		if self.fid is not None:
			self.fid.close()


	def _createCSV(self):
		"""
	Creates the csv output file
		"""
		if self.csvCreated == False:
			self.fid = open(self.fileOut,'w')
			self.csvCreated = True


	def _createHeader(self,fid=None):
		"""
	This method creates the header based off of the previously defined fields.
		"""

		for ind, field in enumerate(self.header):
			self._setField(field)
			if ind != len(self.header) - 1:
				self._nextField(fid)
		self._nextEntry(fid)


	def _nextField(self,fid = None):
		"""
	This method appends a comma to the file output.  Thus dividing two fields.
		"""
		if fid is None:
			fid = self.fid
		fid.write(',')


	def _nextEntry(self,fid = None):
		"""
	This method appends a new line to the file output.  Thus dividing two entires.
		"""
		if fid is None:
			fid = self.fid
		fid.write('\n')

	def _setField(self,field,fid = None):
		"""
	This method writes the input text to the file output.
		"""
		if fid is None:
			fid = self.fid
		fid.write(field)


	def iterText(self,keyIn,textIn=None):
		"""
	This uses the indices ivar to output a splice of the text stream.
		"""
		try:
			key1 = self.indices[keyIn][0]
			key2 = self.indices[keyIn][1]
			if textIn is None:
				return self.text[key1:key2]
			else:
				return textIn[key1:key2]
		except KeyError:
			print("Set the indices first.")


	def setHeader(self,listIn):
		"""
	Set header variable

	List in defines the fields that will appear on the header.
		"""
		self.header = listIn


	def setIndices(self,dictIn):
		"""
	Set indices variable

	Dictionary in defines how each line of text will be spliced.
		"""
		self.indices = dictIn


	def writeToCSV(self,textIn):
		"""
	This method accepts an incoming string and wraps around the setText
	and setEntry method.  It passes the incoming string to the setText method.		
		"""
		self._setText(textIn)
		self._setEntry()


	def _setText(self,textIn):
		"""
	This method sets the text variable to the value passed to it by the
	writeToCSV method
		"""
		self.text = textIn

	def _setEntry(self):
		"""
	This is method manages the data written to the csv file.  It saves the
	customer and item data to be used on other entries
		"""
		for ind, field in enumerate(self.header):
			self._setField(field)
			if ind != len(self.header) - 1:
				self._nextField()
		self._nextEntry()