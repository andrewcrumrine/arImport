"""
	arBuilder.py

	Accounts Receivable Builder Module
	----------------------------------

	This module manages building the csv files necessary to import
	open accounts receivable data into NetSuite via Smart Client

"""

import csvCreator as csv
import stringMan as s

PAYMENT 	= "PMT"
INVOICE 	= "INV"
CREDIT 		= "CRM"
INV_TERM 	= '*'
ACCT_TERM	= 'TOTAL'

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
		self.account = None
		self.headers = ['Customer','Invoice','Invoice Date','Transaction Date'\
		,'Amount','Open Balance']
		self.indices = {'Customer':[0,8],'Invoice':[0,8], 'Code':[8,13],\
		'IDate':[13,23],'Type':[8,12],'TDate':[23,33],'Amount':[33,50],\
		}

	def __del__(self):
		"""
	This method closes the open csv file
		"""
		if self.fid is not None:
			self.fid.close()

	def writeToCSV(self,textIn):
		"""
	Accepts incoming string and manages writing to csv
		"""
		self._setText(textIn)
		if self.account is not None:
			if not self.account.building:
				self.printEntry()
		else:
			self._buildAccount(textIn)
	
	def _buildAccount(self,textIn):
		"""
	Method that manages the account building process
		"""
		if self.account is None and self._isCustomer():
			customer = self.iterText('Customer')
			self.account = OpenAccount(customer)

		elif self.account is not None:
			if self._isCustomer() and not self.account.building:
				self.account = OpenAccount(customer)


	def _isCustomer(self):
		"""
	Checks to see if the incoming text contains a customer number
		"""
		textIn = self.iterText('Customer')
		textIn = s.removeSpaces(textIn)
		if len(textIn) < 8:
			return True
		return False

	def printEntry(self):
		"""
	Diagnostic tool to print entry
		"""
		pass

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
		self.customer = s.removeSpaces(customer)
		self.invoices = []
		self.building = True

	def _addInvoice(self,invoice,date):
		"""
	Creates an invoice and adds it to the list
		"""
		newInvoice = Invoice(invoice,date)
		if not newInvoice.building:
			self.building = False
			return
		self.invoices.append(newInvoice)


	def _addTransToInvoice(self,tranType,date,amount):
		"""
	Calls transaction builder to invoice object
		"""
		self.invoices[-1]._addTransaction(tranType,date,amount)


class Invoice(object):
	"""
	This class is an invoice.
	"""
	def __init__(self,invoice,date):
		"""
	This initializes the invoice.
		"""		
		self.invoice = s.removeSpaces(invoice)
		self.items = []
		self.transactions = []
		self.balance = 0
		self.date = s.removeSpaces(date)
		self.lateCode = 0
		self.termKey = ACCT_TERM
		self.building = self._isTerminator(invoice)

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
		if not newTrans.building:
			self.building = False
			return
		self.transactions.append(newTrans)
		self._correctBalance(newTrans)

	def _correctBalance(self,tranIn):
		"""
	Adds the transaction amount to the bottom line
		"""
		self.balance += tranIn.amount

	def _isTerminator(self,textIn):
		"""
	Checks to see if the new invoice is the terminator
		"""
		if textIn.find(self.termKey) == -1:
			return False
		return True

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
		self.termKey = INV_TERM
		self.building = True

	def setAmount(self,amount):
		"""
	Sets amount variable.  Sets variable to a real number
		"""
		amount = s.removeSpaces(amount)
		amount = s.removeMinus(amount)
		if self._isTerminator(amount):
			self.building = False
			return
		if self.transType == PAYMENT or self.transType == CREDIT:
			self.amount = -float(amount)
		else:
			self.amount = float(amount)

	def _isTerminator(self,amount):
		"""
	Looks for the terminating key that determines when the invoice does
	not have any additional transactions.
		"""
		if amount.find(self.termKey) == -1:
			return False
		return True

	def setDate(self,date):
		"""
	Sets date variable
		"""
		date = s.removeSpaces(date)
		self.date = date