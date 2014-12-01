import time
from datetime import datetime
agentAccess = False #session type
loginBool = False 
validAccounts = []
transactionSummary = ["00 000000 000000 00000000                "]
quit = False
withdrawCaps = {'limit':100000}

#will loop until login is inputted into the command line
#sets the loginBool boolean to True if login is successful
def login():
	global loginBool
	global quit
	
	while loginBool == False:
		input = getInput("Please login: \n")
		if input == "login":
			loginBool = True
		elif input == "exit":
			#end the program (can no longer log in)
			quitProgram()
			return
		else:
			print "invalid login\n"
	#end while
#end login


#sets the agentAccess boolean 
# true = agent mode ; false = retail mode
def getSessionType():
	global agentAccess
	global quit
	
	#login is true
	check = False #while loop flag
	while check == False:
		input = getInput("Please enter a session type: \n")
		if input == "exit":
			quitProgram()
			return
		if input == "agent":
			agentAccess = True
			check = True
		elif input == "retail":		
			#leave agentAccess as False
			check = True
		else:
			print "invalid session type\n"
	#end while
#end getSessionType


#read in validAccounts File and store each line as a String in a list called validAccounts
#read froma directory called in
def readInFiles(): #called by the login command
	global validAccounts
	
	file = open("in/validAccounts.txt","r") 
	validAccounts = file.readlines()	
	for i in range(len(validAccounts)):
		validAccounts[i] = validAccounts[i].strip()
	file.close()		
#end readInFiles


#creates a new txt file called validAccounts which contains an updated list of the accounts 
#Creates a new txt file called transactionSummary which contains an updated list of all transactions
#written to a directory called out
def outputFiles(): #called by logout/quitcommands
	global transacionSummary
	filename = "out/transactionSummary/transactionSummary"+datetime.now().strftime("%H%M%S%f")
	file2 = open(filename+".txt", "w")
	for line2 in transactionSummary:
		file2.write(line2+"\n")
	file2.close()
		
#end outputFiles


#Provides prompts that allow agent users to create new accounts
#Adds transactions to transactionSummary list
def create():
	global validAccounts
	global quit
	
	check = False #loop flag; true once valid input is recieved
	accountNumber = ""
	while check == False: #loops through, checking that account # given is valid and does not exist
		accountNumber = getInput("Enter new account number: \n")
		if accountNumber == "exit":
			quitProgram()
			return
		if isValidAccountNumber(accountNumber):
			if len(accountNumber) < 6:	#adds leading zeros to account number if less than 6 digits
				accountNumber = '0'*(6-len(accountNumber)) + accountNumber 
			if accountNumber in validAccounts:
				print "Account already exists\n"
			else:
				validAccounts.append(accountNumber)
				check = True
		else:
			print "Invalid account number\n"
	#end while
	
	accountName = getAccountName() #get a correctly formated accountName
	if quit == False:
		addTransaction("04", accountNumber, "000000", "00000000", accountName)
#end create


#Provides prompts that allow agent users to delete existing accounts
#Adds transaction to transactionSummary list
def delete():
	global validAccounts
	global quit
	
	prompt = ("Enter the accountNumber you wish to delete: \n")
	accountNumber = getAccountNumber(prompt)
	
	if quit == False: #this is used for testing purposes in order to exit mid program 							
		accountName = getAccountName() #get a correctly formated accountName
		if quit == False:
			validAccounts.remove(accountNumber)
			addTransaction("05", accountNumber, "000000", "00000000", accountName)
#end delete
		

#Provides prompts that allow users to deposits an amount in cents into an existing account
#adds transaction to the transactionSummary list
def deposit():
	global agentAccess
	global validAccounts
	global quit
	
	prompt = "Enter the Account Number: \n"
	accountNumber = getAccountNumber(prompt)
	
	if quit == False: #this is used for testing purposes in order to exit mid program
		check = False #loop flag; true once valid input is recieved
		#get the amount in cents they wish to deposit
		while check ==False:
			cAmount = getNumberInput("Enter the amount you wish to deposit in cents: \n")
			if cAmount == "exit":
				quitProgram()
				return
			if len(cAmount) < 8:	#adds leading zeros to account number if less than 6 digits
				cAmount = '0'*(8-len(cAmount)) + cAmount 
					
			if int(cAmount) > 100000:
				if agentAccess == False:
					print "Cannot deposit more than 100000 cents in retail mode\n"
				elif int(cAmount)>999999:
					print "Cannot transfer over 999999 cents\n"
				else: #agent access
					addTransaction("01", accountNumber, "000000", cAmount, "               ")
					check = True
			else: #cAmount < 100000
				addTransaction("01", accountNumber, "000000", cAmount, "               ")
				check = True
		#end while
	
#end deposit

# Provides prompts that allow users towithdraws an amount in cents from an existing account
#adds transaction to the transactionSummary list
def withdraw():
	global agentAccess
	global validAccounts
	global quit
	global withdrawCaps
	
	prompt = "Enter the Account Number: \n"
	accountNumber = getAccountNumber(prompt)
	
	if quit == False: #this is used for testing purposes in order to exit mid program
		check = False #loop flag; true once valid input is recieved
		#get the amount in cents they wish to deposit
		while check ==False:
			cAmount = getNumberInput("Enter the amount you wish to withdraw in cents: \n")
			if cAmount == "exit":
				quitProgram()
				return
			if len(cAmount) < 8:	#adds leading zeros to account number if less than 6 digits
				cAmount = '0'*(8-len(cAmount)) + cAmount 
				
			if agentAccess == False:
				remainingCap = withdrawCaps['limit'] - getUsedCap(accountNumber)
				if int(cAmount) > 100000: 
					print "Cannot withdraw more than 100000 cents in retail mode\n"
				elif int(cAmount) > int(remainingCap):
					print "Cannot withdraw more than 100000 cents in single retail session\n"
					return
				else:
					addTransaction("02", accountNumber, "000000", cAmount, "               ")
					check = True
			else: 
				if int(cAmount) > 999999:
					print "Cannot withdraw over 999999 cents\n"
				else:
					addTransaction("02", accountNumber, "000000", cAmount, "               ")
					check = True
		#end while	
#end withdraw


# Provides prompts that allow users totransfers an amount in cents from 1 account to a different account
#adds transaction to the transactionSummary list
def transfer():
	
	global agentAccess
	global validAccounts
	global quit
	global withdrawCaps
	
	prompt = "Enter the account number you wish to withdraw from: \n"
	accountNumber = getAccountNumber(prompt)
	if quit == False: #this is used for testing purposes in order to exit mid program
		#check that the account numbers do not macth
		check = False #loop flag; true once valid input is recieved
		while check == False:
			prompt2 = "Enter the account number you wish to deposit to: \n"
			accountNumber2 = getAccountNumber(prompt2)
			if quit == True:
				return
			if accountNumber !=accountNumber2:
				check = True
			else:
				print "Both account number may not be the same\n"
		#end while
		
		check = False
		#get the amount in cents they wish to deposit
		while check ==False:
			cAmount = getNumberInput("Enter the amount you wish to transfer in cents: \n")
			if cAmount == "exit":
				quitProgram()
				return
			if len(cAmount) < 8:	#adds leading zeros to account number if less than 6 digits
				cAmount = '0'*(8-len(cAmount)) + cAmount 
			if agentAccess == False:
				remainingCap = withdrawCaps['limit'] - getUsedCap(accountNumber)
				if int(cAmount) > 100000: 
					print "Cannot transfer more than 100000 cents in retail mode\n"
				elif int(cAmount) > int(remainingCap):
					print "Cannot transfer more than 100000 cents in single retail session\n"
					return
				else:
					addTransaction("03", accountNumber2, accountNumber, cAmount, "               ")
					check = True
			else: 
				if int(cAmount) > 999999:
					print "Cannot transfer over 999999 cents\n"
				else:
					addTransaction("03", accountNumber2, accountNumber, cAmount, "               ")
					check = True
		#end while	
#end transfer


#verifies that the account number exisit in the validAccounts file
#returnsthe correctly formatted existing accountNumber
#will prompt the user for an existing account number until it is recieved
def getAccountNumber(prompt):	
	global agentAccess
	global validAccounts
	
	check = False #loop flag; true once valid input is recieved
	accountNumber = " "
	#get the account number
	while check == False:
		accountNumber = getInput(prompt)
		if accountNumber == "exit":
			quitProgram()
			return
		else:
			if isValidAccountNumber(accountNumber):
				if len(accountNumber) < 6:	#adds leading zeros to account number if less than 6 digits
						accountNumber = '0'*(6-len(accountNumber)) + accountNumber 
				if accountNumber in validAccounts:
						if accountNumber == "000000":
							print "Cannot perform any transactions on account 000000\n"
						else:	#existing account that is not 000000
							check = True
				else: #account number does not exist
					print "The Account number does not exist\n"
			else:
				print "Invalid account number\n"
	#end while
	
	return accountNumber
#end getAccountNumber

#Will prompt the user for a valid account name until it is received
#Returns the correctly formatted accountName
def getAccountName():
	check = False #resets check to use for next while
	accountName = ""
	while check == False: #loops to check that input given is a valid name (only constraint at the moment is length)
		accountName = getInput("Enter account name: \n")
		if accountName == "exit":
			quitProgram()
			return
		if isValidName(accountName):
			if len(accountName) < 15: #adds trailing spaces to name if less than 15 characters
				accountName = accountName + ' '*(15-len(accountName))
			check = True
		else:
			print "Invalid name. Must be between 1 and 15 characters\n"
	#end while	
	return accountName
#end getAccountName

#adds the a transaction to the transaction summary list
def addTransaction(type, accountNumber, accountNumber2, cAmount, name):
	global withdrawCaps
	global agentAccess
	
	if agentAccess == False and type == "02":
		if accountNumber in withdrawCaps:
			withdrawCaps[accountNumber] = withdrawCaps[accountNumber] + cAmount
		else: 
			withdrawCaps[accountNumber] = cAmount
	elif agentAccess == False and type == "03":
		if accountNumber2 in withdrawCaps:
			withdrawCaps[accountNumber2] = withdrawCaps[accountNumber2] + cAmount
		else: 
			withdrawCaps[accountNumber2] = cAmount
	transactionSummary.insert(0, type+" "+accountNumber+" "+accountNumber2+" "+cAmount+" "+name)
	print "transaction submitted\n"
#end addTransaction

#checks the total amount withdrawn from the account
#ensures that the limit for a retail session has not been exceeded
def getUsedCap(accountNum):
	global withdrawCaps
	
	if accountNum in withdrawCaps:
		return int(withdrawCaps[accountNum])
	else:
		return 0
#end getUsedCaps

#Checks if given account number is valid
def isValidAccountNumber(num):
	if len(num) > 6:
		return False
	elif num.isdigit() == False: #account number can only contain digits
		return False
	elif num[0] == 0:
		return False
	return True
#end isValidAccountNumber

#Checks if given name is valid
def isValidName(name):
	if len(name) > 15 or len(name) < 1:
		return False
	return True
#end isValidName


#Gets input from user
def getInput(prompt):
	input = raw_input(prompt)
	input = input.strip()
	input = input.lower()
	return input
#end getInput

def getNumberInput(prompt):
	check = False
	while (check == False): 
		input = raw_input(prompt)
		input = input.strip()
		input = input.lower()
		if input == "exit":
			return input
		#input = input.lstrip("0")
		if input.isdigit():
			check = True
		else:
			print("invalid amount\n")
	return input
#end getNumberInput

def quitProgram():
	global quit
	quit = True
	print "exiting program"


#input File = validAccounts file
#Output File  = updated validAccounts file and transactionSummary file
# In the program we continuously call main (prompting the user to login) until our quit variable becomes True. 
#Once inside main we prompt the user for different valid transactions
#The only way to exit the main function is to input the quit or logout command. 
#once the logout command is recievedd the withdrawl limit dictionary is cleared
def main():
		global loginBool
		global agentAccess
		global quit
		global validAccounts
		global withdrawCaps
		global transactionSummary
		
		login()
		if (quit == False):
			getSessionType()
			if (quit == False): 
				readInFiles()
				while loginBool == True and quit == False:
					input = getInput("Please enter a command: \n")
					if input == "create":
						#only agents have access
						if agentAccess == False:
							print "you do not have permission to perform this action\n"
						else:
							create()
					elif input == "delete":
						#only agents have access
						if agentAccess == False:
							print "you do not have permission to perform this action\n"
						else:
							delete()
					elif input == "deposit":
						deposit()
					elif input == "withdraw":
						withdraw()
					elif input == "transfer":
						transfer()
					elif input == "logout":
						#logout of program
						loginBool = False
						#reset the withdraw limit for all accounts
						withdrawCaps = withdrawCaps = {'limit':100000}
						outputFiles()
						transactionSummary = ["00 000000 000000 00000000                "]
						withdrawCaps = {'limit':100000}
					elif input == "exit":
						#end the program (can no longer log in)
						loginBool = False
						quitProgram()
						return
					else:
						print "invalid input\n"
				#end while
			#end if
		#end if

#end main

#main will be called unless we have called the quit command
while quit == False:
	main()
#end

