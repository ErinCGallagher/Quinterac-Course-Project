import os
import sys
masterAccount = []


#read in the masterAccount file 
#seperate info into tuple (account #, balance, name)
def readInMaster():
	global masterAccount
	
	with open("in/masterAccounts.txt") as file:
		for line in file:
			line = line.rstrip()
			masterAccount.append((line[0:6].lstrip("0"), int(line[7:15]),line[16:].strip()))
#end readInMaster

#read in all transaction summary files and create the merged transaction summary file
def createTransSum():
	file2 = open("out/mergedTSum.txt", "w")
	path="out/transactionSummary"
	dirList = os.listdir(path)
	for file in dirList: #loop through all files in directory
		with open(path+"/"+file) as file:
			for line in file:
				if line[0:2] != "00":
					file2.write(line)
	file2.write("00 000000 000000 00000000                ")	
	file2.close()

#end readInTransSum()

#read in the merged transaction summary file
# execute each line on the this file as it is read from the file 
def executeMergeTransSum():
	with open("out/mergedTSum.txt") as file:
		for line in file:
			execute(line[0:2], line[3:9].lstrip("0"), line[10:16].lstrip("0"), int(line[17:25]), line[26:].strip())

#end executeMergeTransSum()

#determines whcih transaction occured based on the op (operation) number
def execute(op, account1, account2, balance, name):
	if op == "01":
		deposit(account1, balance,0)
	elif op == "02":
		withdraw(account1, balance,0)
	elif op == "03":
		transfer(account1, account2, balance)
	elif op == "04":
		create(account1, name)
	elif op == "05":
		delete(account1, name)
	else:
		print "end of transaction summary file"
#end execute


#deposit money into an existing account
#error terminal log if account does not exist
#transfer ==1 means coming from a transfer transaction
def deposit(account1, balance,transfer):
	global masterAccount

	index = accountExists(account1)
	if index >=0: #account exists
		account = masterAccount[index]
		if account[1] + balance > 99999999: 
			if transfer == 0: #deposit
				sys.exit("Deposit not completed, funds exceeding the possible limit")
			else: #from transfer
				sys.exit("Transfer not completed, funds exceeding the possible limit")
		else:
			masterAccount[index] = (account[0], account[1] + balance, account[2])
	else: #account does not exist
		if  transfer ==0: #deposit
			sys.exit("Deposit not compelted, Account doesn't exist")
		else: #from transfer
			sys.exit("Transfer not completed, Account doesn't exist")
#end deposit


#withdraw money from an existing account
#error terminal log if account does not exist or withdraw results in negative balance
#transfer ==1 means coming from a transfer transaction
def withdraw(account1, balance,transfer):
	global masterAccount

	index = accountExists(account1)
	if index >=0: #account exists
		account = masterAccount[index]
		newBalance= account[1] - balance
		if newBalance >=0: #cannot have a negative balance
			masterAccount[index] = (account[0], newBalance, account[2])
		else:
			if transfer == 0: #withdraw
				sys.exit("Withdaw not completed, insufficient funds")
			else: #from transfer
				sys.exit("Transfer not completed, insufficient funds")
	else:#account does not exist
		if transfer == 0: #withdraw
			sys.exit("Withdraw not completed, Account does not exist")
		else: #from transfer
			sys.exit("Transfer not completed, Account does not exist")
#end withdraw


#transfers balance from accountNum2 to accountNum1
#error terminal log if either account does not exist or withdraw results in negative balance
def transfer(account1, account2, balance):
	withdraw(account2, balance, 1)
	deposit(account1, balance, 1)	
#end transfer


#create a new account and add it to the masterAccount file
#error terminal log if account exists already
def create(account1, name):
	global masterAccount
	
	index = accountExists(account1)
	if index >=0:
		sys.exit("Create not completed, account already exists")
	else: #account number does not exist
		#new account is the smallest 
		if account1 < masterAccount[0][0]:
			masterAccount = [(account1, "0", name)] + masterAccount 
		else:
			i = 1
			flag = False #determines if the account number has been inserted
			#loop until the new account position is located
			while i < len(masterAccount): 
				#insert the account number before the account number larger than it
				if masterAccount[i][0] > account1:
					masterAccount.insert(i,(account1, "0", name))
					flag = True
					i = len(masterAccount)
				i= i+1
			if flag ==False: #new account number is the largest
				masterAccount.insert(i-1,(account1, "0", name))
#end create


#delete an existing account
#error terminal log if account does not exits, account balance is not zero, or name does not macth
def delete(account1, name):	
	global masterAccount

	index = accountExists(account1)
	#account exists
	if index >= 0:
		print("account index >=0, account exists")
		account = masterAccount[index]
		if account[1] == 0: #ensure acount balance is 0
			print("account balance == 0")
			if account[2] == name: #ensure account name matches
				print("account name match masterAccounts file")
				masterAccount.remove((account[0],account[1],account[2]))
			else:
				print("account name does not match masterAccounts file")
				sys.exit("Delete not completed, name does not match account name")
		else: #account balance is not zero
			print("account balance does not = 0")
			sys.exit("Delete not completed, balance is not zero")
	else: #account does not exist
		print("account index < 0, account does not exist")
		sys.exit("Delete not comepleted, account does not exist")
#end delete


#determines if the account exists in the master Account file
#returns index of account in masterAccount if exists and -1 if it does not exist
def accountExists(accountNum):
	global masterAccount
	index =0
	for i in masterAccount:
		if i[0] == accountNum:
			print("account = i[0]")
			return index
		index +=1
	print("account does not = i[0]")	
	return -1
#end accountExists


#removes the old validAccounts and masterAccount files
#creates updates valid accounts and masterAccounts files
#adds the appropriate formating for all values
def createFiles():
	global masterAccount
	try:
		os.remove("in/validAccounts.txt")
	except OSError:
		pass
	try:
		os.remove("in/masterAccounts.txt")
	except OSError:
		pass
		
	validAccountsFile = open("in/validAccounts.txt", "w")
	masterAccountsFile = open("in/masterAccounts.txt", "w")
	index = 0
	#loop through the new masterAccount svariable
	while index < len(masterAccount)-1 and masterAccount[index][0] != "":
		account = masterAccount[index]
		paddedAccountNum = addPad(account[0], 6, "0", "left")
		paddedAccountBalance = addPad(str(account[1]), 8, "0", "left")
		paddedAccountName = addPad(account[2], 15, " ", "right")
		validAccountsFile.write(paddedAccountNum+"\n")
		masterAccountsFile.write(paddedAccountNum+" "+paddedAccountBalance+" "+paddedAccountName+"\n")
		index = index + 1
	#add the ending 0 accounts to the files
	validAccountsFile.write("000000")
	masterAccountsFile.write("000000 00000000                ")
	validAccountsFile.close()
	masterAccountsFile.close()
#end CreateFiles
	
	
#adds the proper padding to the account number, balance and name
#returns the given string with the appropriate padding
def addPad(givenString, requiredLen, padChar, sideToPad):
	if len(givenString) < requiredLen:
		padding = padChar*(requiredLen-len(givenString))
		if sideToPad == "left":
			return padding+givenString
		elif sideToPad == "right":
			return givenString+padding
		else:
			print "Padding parameter given invalid."
	elif len(givenString) == requiredLen:
		return givenString
	else:
		sys.exit("Account or valid number longer than allowed.")
#end addPad

#MAIN
readInMaster()
createTransSum()
executeMergeTransSum()
createFiles()
