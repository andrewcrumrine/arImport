"""
	arBuilder.py

	Accounts Receivable Builder Module
	----------------------------------

	This module manages building the csv files necessary to import
	open accounts receivable data into NetSuite via Smart Client

"""

import csvCreator as csv

class ARCreator(csv.CSVCreator):
	"""
	Class that manages the creation of the Accounts Receivable 
	csv translated from the AS400 text report.
	"""
	def __init__(self):
		"""
	Initializes arCreator class.
		"""
		csv.CSVCreator.__init__(self)

	def __del__(self):
		"""
	This method closes the open csv file
		"""
		if self.fid is not None:
			self.fid.close()

class OpenAccount(object):
	"""
	This class manages the open account information.  It includes
	invoice number, customer, item list along with associated prices,
	the amount paid and the amount due.
	"""
	def __init__(self,customer):
		"""
	Initializes the OpenAccount class.  Needs the customer Id to be
	inputed to initialize.
		"""
		self.customer = customer
		self.invoice = None
		self.items = []
		self.prices = {}
		self.amtDue = 0
		self.amtPaid = 0