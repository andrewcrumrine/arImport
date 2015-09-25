"""
	arBuilder.py

	Accounts Receivable Builder Module
	----------------------------------

	This module manages building the csv files necessary to import
	open accounts receivable data into NetSuite via Smart Client

"""

import csvCreator as csv
import stringMan as s
import arStructure as aS

CUST_KEY 	= '8'
INV_ONLY	= True

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
		self.header = ['Customer','Invoice','Invoice Date','Transaction Type',\
		'Transaction Date','Amount','Open Balance']
		self.indices = {'Customer':[0,8],'Invoice':[0,8], 'Code':[8,13],\
		'IDate':[13,23],'Type':[8,12],'TDate':[23,33],'Amount':[33,50],\
		}
		self._createCSV()
		self._createHeader()
		self.invFid = None
		self.inv_fn = 'invoiceMap.txt'

	def __del__(self):
		"""
	This method closes the open csv file
		"""
		if self.fid is not None:
			self.fid.close()
		if self.invFid is not None:
			self.invFid.close()

	def writeToCSV(self,textIn,eventState):
		"""
	Accepts incoming string and manages writing to csv
		"""
		#print("--NEW LINE---")
		self._setText(textIn)
		if self.account is not None and eventState == -1 \
			and not self.account.reported:
			self.account.reported = True
		#	True input means only write invoices
			self._setEntry(INV_ONLY)
		else:
			self._buildAccount(eventState)

		# if self.account is not None:
		# 	if self._buildStatus() == -1 and not self.account.reported:
		# 		print("Print entry")
		# 		self.account.reported = True
		# 		#self.printEntry()
		# 		self._setEntry()
		# 	else:
		# 		print("Create new account")
		# 		self._buildAccount()
		# else:
		# 	print("Pass everything else")
		# 	self._buildAccount()
	
	def _buildAccount(self,eventState):
		"""
	Method that manages the account building process
		"""
		if eventState == 0:
			customer = self.iterText('Customer')
			self.account = aS.OpenAccount(customer)

		elif eventState == 1:
			inv = self.iterText('Invoice')
			dte = self.iterText('IDate')
			self.account._addInvoice(inv,dte)

		elif eventState == 2:
			typ = self.iterText('Type')
			dte = self.iterText('TDate')
			amt = self.iterText('Amount')
			self.account._addTransToInvoice(typ,dte,amt)

		# if self.account is None and self._isCustomer():
		# 	print("Create fresh customer")
		# 	customer = self.iterText('Customer')
		# 	print(customer)
		# 	self.account = aS.OpenAccount(customer)

		# elif self.account is not None:
		# 	print(str(self._buildStatus()))
		# 	print(self._isCustomer())
		# 	if self._buildStatus() == -1 and self._isCustomer():
		# 		print("Replace customer with new one")	
		# 		customer = self.iterText('Customer')
		# 		print(customer)
		# 		self.account = aS.OpenAccount(customer)

		# 	elif self._buildStatus() == 0 and not self._isCustomer():
		# 		print("Create new invoice")
		# 		inv = self.iterText('Invoice')
		# 		print(inv)
		# 		dte = self.iterText('IDate')
		# 		print(dte)
		# 		self.account._addInvoice(inv,dte)

		# 	elif self._buildStatus() >= 1 and not self._isCustomer():
		# 		print("Create new transaction")
		# 		typ = self.iterText('Type')
		# 		print(typ)
		# 		dte = self.iterText('TDate')
		# 		print(dte)
		# 		amt = self.iterText('Amount')
		# 		print(amt)
		# 		self.account._addTransToInvoice(typ,dte,amt)


	def _buildStatus(self):
		"""
	Returns the deepest bulid level
		"""
		if self.account is None:
			return -1
		if self.account.building:
			if len(self.account.invoices) > 0:
				if self.account.invoices[-1].building:
					if len(self.account.invoices[-1].transactions) > 0:
						if self.account.invoices[-1].transactions[-1]:
							return 2
					return 1
			return 0
		return -1

	def _isCustomer(self):
		"""
	Checks to see if the incoming text contains a customer number
		"""
		textIn = self.iterText('Customer')
		textIn = s.removeSpaces(textIn)
		if len(textIn) < 1:
			return False
		if textIn[0] == CUST_KEY:
			return True
		return False

	def printEntry(self):
		"""
	Diagnostic tool to print entry
		"""
		print self.account.customer
		for inv in self.account.invoices:
			for trans in inv.transactions:
				print inv.invoice + '\t' + inv.date + '\t' + trans.transType \
				+ '\t' + trans.date + '\t' + str(trans.amount) + '\t' + \
				str(inv.balance)

	def _setInvoiceMap(self,inv):
		"""
	Method writes to the text file used to create the invoice map
		"""
		if self.invFid is not None:
			self.invFid.write(inv.invoice)
			self.invFid.write('\t')
			self.invFid.write('True')
			self.invFid.write('\n')

	def _setEntry(self,invOnly = False):
		"""
	Sets the entry of the entire account built from the arStructure module.
		"""
		if invOnly and self.invFid is None:
			self.invFid = open(self.inv_fn,'w')

		for inv in self.account.invoices:
			for trans in inv.transactions:
				if invOnly:
					if trans.transType == "INV" and abs(inv.balance) > 5:
						self._setField(self.account.customer); self._nextField()
						self._setField(inv.invoice); self._nextField()
						self._setField(inv.date); self._nextField()
						self._setField(trans.transType); self._nextField()
						self._setField(trans.date); self._nextField()
						self._setField(str(round(trans.amount,2))); self._nextField()
						self._setField(str(round(inv.balance,2))); self._nextEntry()
						self._setInvoiceMap(inv)

				else:
					self._setField(self.account.customer); self._nextField()
					self._setField(inv.invoice); self._nextField()
					self._setField(inv.date); self._nextField()
					self._setField(trans.transType); self._nextField()
					self._setField(trans.date); self._nextField()
					self._setField(str(round(trans.amount,2))); self._nextField()
					self._setField(str(round(inv.balance,2))); self._nextEntry()