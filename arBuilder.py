"""
	arBuilder.py

	Accounts Receivable Builder Module
	----------------------------------

	This module manages building the csv files necessary to import
	open accounts receivable data into NetSuite via Smart Client

"""

import csvCreator as csv
import stringMan as s

PAYMENT = "PMT"
INVOICE = "INV"
CREDIT = "CRM"

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
	invoice numbers, customer, item list along with associated prices,
	the amount paid and the amount due.
	"""
	def __init__(self,customer):
		"""
	Initializes the OpenAccount class.  Needs the customer Id to be
	inputed to initialize.
		"""
		self.customer = customer
		self.invoices = []
		self.building = True

	def _setInvoice(self,invoice):
		"""
	Sets invoice variable
		"""
		self.invoice = invoice

class Invoice(object):
	"""
	This class is an invoice.
	"""
	def __init__(self,invoice):
		"""
	This initializes the invoice.
		"""		
		self.invoice = s.removeSpaces(invoice)
		self.items = []
		self.transactions = []
		self.balence = 0
		self.date = ''
		self.lateCode = 0

	def _setDate(self,date):
		"""
	Sets date variable
		"""
		self.date = s.removeSpaces(date)

	def _setLateCode(self,code):
		"""
	Sets late code variable.  This variable is used to determine how far back
	a search is required.
		"""
		self.lateCode = s.removeSpaces(code)

	def _addTransaction(self,transType,date,amount):
		"""
	Adds a transaction to the transaction list
		"""
		newTrans = InvoiceTrans(self.invoice,transType)
		newTrans.setDate(date)
		newTrans.setAmount(amount)
		self.transactions.append(newTrans)
		self._correctBalence(newTrans)

class InvoiceTrans(object):
	"""
	This class is a transaction against an open invoice.
	"""
	def __init__(self,reference,transType):
		"""
	This initializes the account transaction.  It needs the incoming invoice
	number and transaction type to be created.
		"""
		self.date = ''
		self.invoice = reference
		self.transType = s.removeSpaces(transType)
		self.amount = 0

	def setAmount(self,amount):
		"""
	Sets amount variable.  Sets variable to a real number
		"""
		amount = s.removeSpaces(amount)
		amount = s.removeMinus(amount)
		if self.transType == PAYMENT or self.transType == CREDIT:
			self.amount = -float(amount)
		else:
			self.amount = float(amount)

	def setDate(self,date):
		"""
	Sets date variable
		"""
		date = s.removeSpaces(date)
		self.date = date