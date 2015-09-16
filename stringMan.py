"""
	stringMan.py

	String Manipulation library
	Set of functions used to modifiy strings.

"""

def wcFind(key,wc):
	"""
	This function finds the positions of all wildcards in a string
	"""
	keyOut = []
	index = key.find(wc)
	if index == -1:
		return -1
	wcPos = [index]
	while index != -1:
		key = key[index+1:]
		index = key.find(wc)
		if index != -1:
			wcPos.append(index + wcPos[-1] + 1)
	return wcPos


def addWC(strIn,wcPos,wc):
	"""
	This function replaces a string with a wildcard with the incoming
	positions listed.
	"""
	for pos in wcPos:
		strIn = strIn[:pos] + wc + strIn[pos+1:]
	return strIn


def wildSearch(stringIn, key, wildcard=None):
	"""
	This function searches a string for a key that contains
	wildcard characters.  By default the wildcard is set to None so the
	function behaves like the find function. The wildcard cannot be in
	the first position of the key.

	@param: stringIn String
	@param: key String
	@param: wildcard String

	@return: index int
	"""
	if wildcard == None:
		return stringIn.find(key)

	if key.find(wildcard) == -1:
		return stringIn.find(key)

	try:
		if key[0] != wildcard[0]:
			index = stringIn.find(key[0])
		else:
			index = 0
	except IndexError :
		return -1

	#if index == -1:
	#	return -1

	stringLen = len(stringIn)
	keyPos = wcFind(key,wildcard)
	while len(stringIn) > len(key) and index != -1:
		index = stringIn.find(key[:keyPos[0]])
		strCon =  addWC(stringIn[index:index + len(key)],keyPos,wildcard)
		if strCon == key:
			return index + stringLen - len(stringIn)
		stringIn = stringIn[index + len(key):]

def newWildSearch(stringIn, key, wildcard=None):
	"""
	Expands upon the wild search function in an effort for greater robustness.
	"""
	if wildcard == None:
		return stringIn.find(key)

	if key.find(wildcard) == -1:
		return stringIn.find(key)

	#	Build locations
	keyPos,keyStr = newWCfind(key,wildcard)
	strPos = key.find(keyStr)

	if stringIn.find(keyStr) == -1:
		return -1

	tempStr = ' '*len(key)
	newPos = -1
	while len(key[strPos:]) <= len(tempStr):
		newPos = stringIn.find(keyStr,newPos + 1)
		if newPos >= strPos:
			tempStr = stringIn[newPos - strPos: (newPos - strPos) + len(key)]
			for i in range(0,len(keyPos)):
				tempStr = tempStr[:keyPos[i]] + wildcard + tempStr[keyPos[i] + len(wildcard):]
			if tempStr == key:
				return newPos - strPos

	return -1



def newWCfind(key,wc):
	"""
	Update to wcFind
	"""
	keyPos = []
	keyPosLoc = 0
	maxDist = 0
	keyStr = ''
	for i in range(0,key.count(wc)):
		kPNew = key.find(wc,keyPosLoc)
		if kPNew - keyPosLoc > maxDist:
			keyStr = key[keyPosLoc:kPNew]
			maxDist = kPNew - keyPosLoc
		keyPos.append(kPNew)
		keyPosLoc = kPNew + 1

	if len(key[keyPos[-1]:]) > keyStr:
		keyStr = key[keyPos[-1] + 1:]

	return keyPos,keyStr

def removeSpaces(stringIn):
	"""
	This method searches the incoming text for leading and trailing spaces.
	It returns text without leading and trailing spaces.
	"""
	if len(stringIn) > 0 :
		if stringIn[0] == ' ':
			return removeSpaces(stringIn[1:])
		elif stringIn[-1] == ' ':
			return removeSpaces(stringIn[:-1])
	return stringIn

def removeCommas(textIn):
	"""
	This method searches incoming text for commas and returns text with the
	commas removed.
	"""
	loc = textIn.find(',')
	if loc != -1:
		return removeCommas(textIn[:loc] + textIn[loc+1:])
	return textIn

def removeMinus(textIn):
	"""
	This function searches incoming text for a minus sign and returns text with 
	it removed.
	"""
	loc = textIn.find('-')
	if loc != -1:
		return removeCommas(textIn[:loc] + textIn[loc+1:])
	return textIn

def subStrByChar(textIn,char1,char2):
	"""
	Function returns a substring nestled between two chars
	"""
	return textIn[textIn.find(char1)+len(char1):textIn.find(char2)]